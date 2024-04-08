from behave import given, when, then
from scraping import scraping, get_playlist_url
import os
import pandas as pd


@given('I have a Spotify playlist URL stored in "{file_path}"')
def step_impl_given(context, file_path):
    context.playlist_url = get_playlist_url(file_path)


@when('I scrape the playlist data')
def step_impl_when(context):
    context.output_csv = 'playlist.csv'
    context.result = scraping(context.playlist_url, context.output_csv)


@then('the data should be saved in "{output_csv}"')
def step_impl_then_data_saved(context, output_csv):
    assert os.path.exists(output_csv), f"File '{output_csv}' not found"
    context.df = pd.read_csv(output_csv)


@then('the CSV file should contain the correct columns')
def step_impl_then_correct_columns(context):
    expected_columns = ['title', 'artist', 'album', 'duration', 'album_image']
    assert set(expected_columns).issubset(context.df.columns), "CSV file does not contain expected columns"
