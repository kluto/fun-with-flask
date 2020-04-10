#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for, jsonify, abort
from flask_moment import Moment
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form

from forms import *
from models import db, Artist, Venue, Show
from flask_migrate import Migrate

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db.init_app(app)
migrate = Migrate(app, db)



#----------------------------------------------------------------------------#
# Helper functions
#----------------------------------------------------------------------------#

def venue_show_data(show):
    data = {
        'artist_id': show.artistshow.id,
        'artist_name': show.artistshow.name,
        'artist_image_link': show.artistshow.image_link,
        'start_time': show.start_time
    }
    return data

def artist_show_data(show):
    data = {
        'venue_id': show.venueshow.id,
        'venue_name': show.venueshow.name,
        'venue_image_link': show.venueshow.image_link,
        'start_time': show.start_time
    }
    return data

def past_shows_for_venue(venue_id):
    shows = Show.query.filter(Show.start_time < datetime.now().strftime('%Y-%m-%d %H:%M'), Show.venue_id == venue_id).all()
    return [venue_show_data(show) for show in shows]

def upcoming_shows_for_venue(venue_id):
    shows = Show.query.filter(Show.start_time > datetime.now().strftime('%Y-%m-%d %H:%M'), Show.venue_id == venue_id).all()
    return [venue_show_data(show) for show in shows]

def past_shows_for_artist(artist_id):
    shows = Show.query.filter(Show.start_time < datetime.now().strftime('%Y-%m-%d %H:%M'), Show.artist_id == artist_id).all()
    return [artist_show_data(show) for show in shows]


def upcoming_shows_for_artist(artist_id):
    shows = Show.query.filter(Show.start_time > datetime.now().strftime('%Y-%m-%d %H:%M'), Show.artist_id == artist_id).all()
    return [artist_show_data(show) for show in shows]




#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
    date = dateutil.parser.parse(value)
    if format == 'full':
        format="EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format="EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format)

app.jinja_env.filters['datetime'] = format_datetime


#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
    return render_template('pages/home.html')


#----------------------------------------------------------------------------#
#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
    all_venues = Venue.query.all()
    city_states = {(venue.city, venue.state) for venue in all_venues}
    data = [{'city': cs[0], 'state': cs[1], 'venues': []} for cs in city_states]
    for venue in all_venues:
        for area in data:
            if venue.city == area['city'] and venue.state == area['state']:
                area['venues'].append({
                  'id': venue.id,
                  'name': venue.name,
                  'num_upcoming_shows': len(upcoming_shows_for_venue(venue.id))
                })
    return render_template('pages/venues.html', areas=data);


@app.route('/venues/search', methods=['POST'])
def search_venues():
    search_string = request.form.get('search_term', '')
    venues = Venue.query.filter(Venue.name.ilike('%' + search_string + '%')).all()
    venue_details = [{'id': venue.id, 'name': venue.name, 'num_upcoming_shows': len(upcoming_shows_for_venue(venue.id))} for venue in venues]
    response = {'count': len(venue_details), 'data': venue_details}
    return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    try:
        venue = Venue.query.get(venue_id)
        data = {
            'id': venue.id,
            'name': venue.name,
            'city': venue.city,
            'address': venue.address,
            'genres': venue.genres.split(","),
            'state': venue.state,
            'image_link': venue.image_link,
            'phone': venue.phone,
            'website': venue.website,
            'facebook_link': venue.facebook_link,
            'seeking_talent': venue.seeking_talent,
            'seeking_description': venue.seeking_description,
            'upcoming_shows': upcoming_shows_for_venue(venue.id),
            'upcoming_shows_count': len(upcoming_shows_for_venue(venue.id)),
            'past_shows': past_shows_for_venue(venue.id),
            'past_shows_count': len(past_shows_for_venue(venue.id))
        }
    except:
        abort (404)
    return render_template('pages/show_venue.html', venue=data)


#  Create Venue
#  ----------------------------------------------------------------


@app.route('/venues/create', methods=['GET'])
def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)


@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    error = False
    try:
        new_venue = Venue(
            name=request.form.get('name'),
            city=request.form.get('city'),
            state=request.form.get('state'),
            address=request.form.get('address'),
            genres=",".join(request.form.getlist('genres')),
            phone=request.form.get('phone'),
            facebook_link=request.form.get('facebook_link'),
            image_link=request.form.get('image_link'),
            website=request.form.get('website'),
            seeking_talent=request.form.get('seeking_talent')==True,
            seeking_description=request.form.get('seeking_description')
        )
        db.session.add(new_venue)
        db.session.commit()
    except:
        error = True
        db.session.rollback()
    finally:
        db.session.close()
    if error:
        flash('An error occurred. Venue ' + request.form.get('name') + ' could not be listed.')
    else:
        flash('Venue ' + request.form.get('name') + ' was successfully listed!')
    return render_template('pages/home.html')


@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
    error = False
    try:
        venue = Venue.query.get(venue_id)
        db.session.delete(venue)
        db.session.commit()
    except:
        db.session.rollback()
        error = True
    finally:
        db.session.close()
    if error:
        abort (404)
    else:
        return None


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    try:
        venue = Venue.query.get(venue_id)
        form = VenueForm(
            name=venue.name,
            city=venue.city,
            state=venue.state,
            address=venue.address,
            phone=venue.phone,
            facebook_link=venue.facebook_link,
            website=venue.website,
            image_link=venue.image_link,
            seeking_talent=venue.seeking_talent,
            seeking_description=venue.seeking_description
        )
    except:
        abort (404)
    return render_template('forms/edit_venue.html', form=form, venue=venue)


@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    try:
        venue = Venue.query.filter_by(id=venue_id).all()[0]
        venue.name=request.form.get('name')
        venue.city=request.form.get('city')
        venue.state=request.form.get('state')
        venue.address=request.form.get('address')
        venue.phone=request.form.get('phone')
        venue.facebook_link=request.form.get('facebook_link')
        venue.website=request.form.get('website')
        venue.image_link=request.form.get('image_link')
        venue.seeking_talent=request.form.get('seeking_talent') == 'True'
        venue.seeking_description=request.form.get('seeking_description')
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()
    return redirect(url_for('show_venue', venue_id=venue_id))


#  Artists
#  ----------------------------------------------------------------

@app.route('/artists')
def artists():
    all_artists = Artist.query.all()
    data = [
        {'id': artist.id, 'name': artist.name, 'num_upcoming_shows': len(upcoming_shows_for_artist(artist.id))} for artist in all_artists
    ]
    return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
    search_string = request.form.get('search_term', '')
    artists = Artist.query.filter(Artist.name.ilike('%' + search_string + '%')).all()
    artist_details = [{'id': artist.id, 'name': artist.name, 'num_upcoming_shows': len(upcoming_shows_for_artist(artist.id))} for artist in artists]
    response = {'count': len(artist_details), 'data': artist_details}
    return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    try:
        artist = Artist.query.get(artist_id)
        data = {
            'id': artist.id,
            'name': artist.name,
            'city': artist.city,
            'genres': artist.genres.split(","),
            'state': artist.state,
            'image_link': artist.image_link,
            'phone': artist.phone,
            'website': artist.website,
            'facebook_link': artist.facebook_link,
            'seeking_venue': artist.seeking_venue,
            'seeking_description': artist.seeking_description,
            'upcoming_shows': upcoming_shows_for_artist(artist.id),
            'upcoming_shows_count': len(upcoming_shows_for_artist(artist.id)),
            'past_shows': past_shows_for_artist(artist.id),
            'past_shows_count': len(past_shows_for_artist(artist.id))

        }
    except:
        abort (404)
    return render_template('pages/show_artist.html', artist=data)


@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    try:
        artist = Artist.query.get(artist_id)
        form = ArtistForm(
            name=artist.name,
            city=artist.city,
            state=artist.state,
            phone=artist.phone,
            facebook_link=artist.facebook_link,
            website=artist.website,
            image_link=artist.image_link,
            seeking_venue=artist.seeking_venue,
            seeking_description=artist.seeking_description
        )
    except:
        abort (404)
    return render_template('forms/edit_artist.html', form=form, artist=artist)


@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    try:
        artist = Artist.query.get(artist_id)
        artist.name=request.form.get('name')
        artist.city=request.form.get('city')
        artist.state=request.form.get('state')
        artist.phone=request.form.get('phone')
        artist.facebook_link=request.form.get('facebook_link')
        artist.website=request.form.get('website')
        artist.image_link=request.form.get('image_link')
        artist.seeking_venue=request.form.get('seeking_venue') == 'True'
        artist.seeking_description=request.form.get('seeking_description')
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()
    return redirect(url_for('show_artist', artist_id=artist_id))



#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    error = False
    try:
        new_artist = Artist(
            name=request.form.get('name'),
            city=request.form.get('city'),
            state=request.form.get('state'),
            genres=",".join(request.form.getlist('genres')),
            phone=request.form.get('phone'),
            facebook_link=request.form.get('facebook_link'),
            image_link=request.form.get('image_link'),
            website=request.form.get('website'),
            seeking_venue=request.form.get('seeking_venue')==True,
            seeking_description=request.form.get('seeking_description')
        )
        db.session.add(new_artist)
        db.session.commit()
    except:
        error = True
        db.session.rollback()
    finally:
        db.session.close()
    if error:
        flash('An error occurred. Artist ' + request.form.get('name') + ' could not be listed.')
    else:
        flash('Artist ' + request.form.get('name') + ' was successfully listed!')
    return render_template('pages/home.html')



#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
    all_shows = Show.query.all()
    data =[{
            'venue_id': show.venueshow.id,
            'venue_name': show.venueshow.name,
            'artist_id': show.artistshow.id,
            'artist_name': show.artistshow.name,
            'artist_image_link': show.artistshow.image_link,
            'start_time': show.start_time
    } for show in all_shows]
    return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    error = False
    try:
        new_show = Show(
            start_time=request.form.get('start_time'),
            artist_id=request.form.get('artist_id'),
            venue_id=request.form.get('venue_id'),
        )
        db.session.add(new_show)
        db.session.commit()
    except:
        error = True
        db.session.rollback()
    finally:
        db.session.close()
    if error:
        flash('An error occurred. Show could not be listed.')
    else:
        flash('Show was successfully listed!')
    return render_template('pages/home.html')


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
