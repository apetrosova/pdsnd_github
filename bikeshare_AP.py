#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

import time
import pandas as pd
import numpy as np

MONTHS = ['January', 'February', 'March', 'April', 'May', 'June']
DAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
CITY_DATA = { 'Chicago': 'chicago.csv',
              'New York City': 'new_york_city.csv',
              'Washington': 'washington.csv' }

def get_valid_input(valid_values, prompt):
    """Get users input from a list of valid values. 
        This function verifies if the entry is valid and prompts user to reenter the value if invalid.

    INPUT:
    valid_values: list. List of valid input values
    prompt: str. Text message to show before input

    OUTPUT:
    str. Returns value from the list selected by user
    """
    print(prompt)
    while True: 
        s = input()
        if s.title() in valid_values or s.lower() in valid_values:
            break
        else:
            print('Invalid input, please try again from the follwoing: ', valid_values)
    return s.title()

def get_filters():
    """Asks user to specify a city, month, and day to analyze.
    
    INPUT:
    NA

    OUTPUT:
    city: str. Name of the city to analyze
    month: str. Name of the month to filter by, or "All" to apply no month filter
    day: str. Name of the day of week to filter by, or "All" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city =  get_valid_input(list(CITY_DATA.keys()), 'Please choose a city from the following: Chicago, New York City, Washington > ')

    # get user input for month (all, january, february, ... , june)
    month = get_valid_input(MONTHS + ['all'], 'Please choose a month from January through June or all for no filter > ')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = get_valid_input(DAYS + ['all'], 'Please choose a day of week or all for no filter > ')

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """Loads data for the specified city and filters by month and day if applicable.

    INPUT:
    city: str. Name of the city to analyze
    month: str. Name of the month to filter by, or "All" to apply no month filter
    day: str. Name of the day of week to filter by, or "All" to apply no day filter

    OUTPUT:
    df: Pandas DataFrame. City data filtered by month and day
    """
    # load data file into a dataframe
    filename = CITY_DATA[city]
    df = pd.read_csv(filename)

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    
    #filter by month if applicable
    if month != 'All':
        # use the index of the months list to get the corresponding int
        month_num = MONTHS.index(month.title())+1
    
        # filter by month to create the new dataframe
        df = df[df.month == month_num]
    
    # filter by day of week if applicable
    if day != 'All':
        # filter by day of week to create the new dataframe
        df = df[df.day_of_week == day.title()]
    
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel.
    
    INPUT:
    df: DataFrame. Input data  
    """

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    
    # prepare columns that will used by this function
    if df['Start Time'].dtype == 'object':
        df['Start Time'] = pd.to_datetime(df['Start Time'])
    if 'month' not in df.columns:
        df['month'] = df['Start Time'].dt.month
    if 'day_of_week' not in df.columns:
        df['day_of_week'] = df['Start Time'].dt.weekday_name
    if 'hour' not in df.columns:
        df['hour'] = df['Start Time'].dt.hour

    # display the most common month
    popular_month = df['month'].mode()[0]

    # display the most common day of week
    popular_dayofweek = df['day_of_week'].mode()[0]

    # display the most common start hour
    popular_start_hour = df['hour'].mode()[0]
    
    print('Most Popular Month:', MONTHS[popular_month-1])
    print('Most Popular Day of Week:',  popular_dayofweek)
    print('Most Popular Start Hour:', popular_start_hour)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip.
    
    INPUT:
    df: DataFrame. Input data  
    """

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]

    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]

    # display most frequent combination of start station and end station trip
    popular_trip = df.groupby(['Start Station', 'End Station']).size().sort_values(ascending=False).index[0]
   
    print('Most Popular Start Station:', popular_start_station)
    print('Most Popular End Station:',  popular_end_station)
    print('Most Popular Trip: {} >>> {}'.format(*popular_trip))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration.
    
    INPUT:
    df: DataFrame. Input data  
    """

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel = df['Trip Duration'].sum()

    # display mean travel time
    mean_travel = df['Trip Duration'].mean()

    print('Total Travel Time:', total_travel)
    print('Mean Travel Time:', mean_travel)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users.
    
    INPUT:
    df: DataFrame. Input data  
    """

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    ut = zip(user_types.index, user_types)
    ut_result = '\n'.join('  {:12} {}'.format(*x) for x in list(ut))
    
    # Display counts of gender
    if 'Gender' in df.columns:
        gender_types = df['Gender'].value_counts()
        gt = zip(gender_types.index, gender_types)
        gt_result = '\n'.join('  {:12} {}'.format(*x) for x in list(gt))
    else:
        gt_result = 'Gender data is not available'

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        earliest_yob = int(df['Birth Year'].min())
        recent_yob = int(df['Birth Year'].max())
        common_yob = int(df['Birth Year'].mode()[0])
        yob_result = 'Birth Year: Earliest - {}, Most Recent - {}, Most Common - {}'.format(earliest_yob,  recent_yob, common_yob)
    else:
        yob_result = 'Birth Year data is not available'

    print('Counts of User Types:\n{}\n'.format(ut_result))
    print('Counts of Genders:\n{}\n'.format(gt_result))
    print(yob_result)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df):
    """Displaying raw data by 5 rows at a time.
        This function prompts user to continue to show next block of rows.

    INPUT:
    df: pandas DataFrame. Data to display    
    """
    current_position = 0
    display_size = 5
    rows_count = df.shape[0]
    show_data = input('Would you like to see raw data (total = {})? Enter yes or no.\n'.format(rows_count)).lower()
    while current_position < rows_count and show_data == 'yes':
        # use temporary Pandas context formating to prevent colapsing middle columns on the display
        with pd.option_context('display.max_rows', None, 'display.max_columns', None):
            print(df[current_position:current_position+display_size:])
        current_position += display_size    
        show_data = input('Would you like to see more data? Enter yes or no.\n').lower()

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)    
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
