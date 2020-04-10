from app import db, Venue, Artist, Show
 
v1dict = {
  "name": "The Musical Hop",
  "city": "San Francisco",
  "state": "CA",
  "address": "1015 Folsom Street",
  "phone": "123-123-1234",
  "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
  "facebook_link": "https://www.facebook.com/TheMusicalHop",
  "genres": ",".join(["Jazz", "Reggae", "Swing", "Classical", "Folk"]),
  "website": "https://www.themusicalhop.com",
  "seeking_talent": True,
  "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
  "past_shows_count": 0,
  "upcoming_shows_count": 0,
}
Venue1 = Venue(**v1dict)


v2dict = {
  "name": "The Dueling Pianos Bar",
  "city": "New York",
  "state": "NY",
  "address": "335 Delancey Street",
  "phone": "914-003-1132",
  "image_link": "https://images.unsplash.com/photo-1497032205916-ac775f0649ae?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80",
  "facebook_link": "https://www.facebook.com/theduelingpianos",
  "genres": ",".join(["Classical", "R&B", "Hip-Hop"]),
  "website": "https://www.theduelingpianos.com",
  "seeking_talent": False,
  "past_shows_count": 0,
  "upcoming_shows_count": 0,
  }
Venue2 = Venue(**v2dict)


v3dict = {
  "name": "Park Square Live Music & Coffee",
  "city": "San Francisco",
  "state": "CA",
  "address": "34 Whiskey Moore Ave",
  "phone": "415-000-1234",
  "website": "https://www.parksquarelivemusicandcoffee.com",
  "image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
  "facebook_link": "https://www.facebook.com/ParkSquareLiveMusicAndCoffee",
  "genres": ",".join(["Rock n Roll", "Jazz", "Classical", "Folk"]),
  "seeking_talent": False,
  "past_shows_count": 0,
  "upcoming_shows_count": 0,
  }
Venue3 = Venue(**v3dict)


a1dict = {
  "name": "Guns N Petals",
  "genres": ",".join(["Rock n Roll"]),
  "city": "San Francisco",
  "state": "CA",
  "phone": "326-123-5000",
  "website": "https://www.gunsnpetalsband.com",
  "facebook_link": "https://www.facebook.com/GunsNPetals",
  "seeking_venue": True,
  "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
  "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
  "past_shows_count": 0,
  "upcoming_shows_count": 0,
}
Artist1 = Artist(**a1dict)


a2dict = {
  "name": "Matt Quevedo",
  "genres": ",".join(["Jazz"]),
  "city": "New York",
  "state": "NY",
  "phone": "300-400-5000",
  "facebook_link": "https://www.facebook.com/mattquevedo923251523",
  "seeking_venue": False,
  "image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
  "past_shows_count": 0,
  "upcoming_shows_count": 0,
}
Artist2 = Artist(**a2dict)


a3dict = {
  "name": "The Wild Sax Band",
  "genres": ",".join(["Jazz", "Classical"]),
  "city": "San Francisco",
  "state": "CA",
  "phone": "432-325-5432",
  "seeking_venue": False,
  "image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
  "past_shows_count": 0,
  "upcoming_shows_count": 0,
}
Artist3 = Artist(**a3dict)


# db.session.add(Venue1)
# db.session.add(Venue2)
# db.session.add(Venue3)
# db.session.add(Artist1)
# db.session.add(Artist2)
# db.session.add(Artist3)


db.session.commit()
db.session.close()



    # data=[{
    #     "venue_id": 1,
    #     "venue_name": "The Musical Hop",
    #     "artist_id": 4,
    #     "artist_name": "Guns N Petals",
    #     "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
    #     "start_time": "2019-05-21T21:30:00.000Z"
    # }, {
    #     "venue_id": 3,
    #     "venue_name": "Park Square Live Music & Coffee",
    #     "artist_id": 5,
    #     "artist_name": "Matt Quevedo",
    #     "artist_image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
    #     "start_time": "2019-06-15T23:00:00.000Z"
    # }, {
    #     "venue_id": 3,
    #     "venue_name": "Park Square Live Music & Coffee",
    #     "artist_id": 6,
    #     "artist_name": "The Wild Sax Band",
    #     "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    #     "start_time": "2035-04-01T20:00:00.000Z"
    # }, {
    #     "venue_id": 3,
    #     "venue_name": "Park Square Live Music & Coffee",
    #     "artist_id": 6,
    #     "artist_name": "The Wild Sax Band",
    #     "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    #     "start_time": "2035-04-08T20:00:00.000Z"
    # }, {
    #     "venue_id": 3,
    #     "venue_name": "Park Square Live Music & Coffee",
    #     "artist_id": 6,
    #     "artist_name": "The Wild Sax Band",
    #     "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    #     "start_time": "2035-04-15T20:00:00.000Z"
    # }]