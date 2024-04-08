Feature: Scraping Spotify Playlist Data
  As a user
  I want to scrape data from a Spotify playlist
  So that I can analyze the playlist contents

  Scenario: Scrape Spotify Playlist Data
    Given I have a Spotify playlist URL stored in "playlist_url.txt"
    When I scrape the playlist data
    Then the data should be saved in "playlist.csv"
    And the CSV file should contain the correct columns