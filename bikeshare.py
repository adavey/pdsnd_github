import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

months = ['january', 'february', 'march', 'april', 'may', 'june']  
days = ['monday','tuesday','wednesday','thursday','friday','saturday','sunday']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = ""
    while city.lower() not in CITY_DATA.keys():
        try:
            city = input("Enter city to explore (chicago, new york city, washington): ")
            if city.lower() not in CITY_DATA.keys():
                print(f"{city} is not a valid entry.  Please select a city from the list.")

        except KeyboardInterrupt:
            print("\nExiting program.")
            quit()


    # get user input for month (all, january, february, ... , june)
    month = ""
    while month.lower() not in months and month.lower() != 'all':
        try:
            month = input("Enter month to explore (all, january, february, ... , june): ")
            if month.lower() not in months and month.lower() != 'all':
                print(f"{month} is not a valid entry.  Please select 'all' or a month between January and June.")

        except KeyboardInterrupt:
            print("\nExiting program.")
            quit()       

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = ""
    while day.lower() not in days and day.lower() != 'all':
        try:
            day = input("Enter day (all, monday, tuesday, ... sunday): ")
            if day.lower() not in days and day.lower() != 'all':
                print(f"{day} is not a valid entry.  Please select 'all' or a day between Monday and Sunday.")
 
        except KeyboardInterrupt:
            print("\nExiting program.")
            quit()  
    


    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # read csv file associated with selected city
    df = pd.read_csv(CITY_DATA[city.lower()])

    # convert Birth Year from float to int
    if 'Birth Year' in df.columns:  # test for Birth Year column as Washington data does not have this info
        df['Birth Year'] = df['Birth Year'].fillna(0).astype(int)

    # convert start and end time columns to date time data types
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    # extract hour, month and day of week from Start Time and add as new columns
    df['hour'] = df['Start Time'].dt.hour
    df['month'] = df['Start Time'].dt.month_name()
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if specified
    if month != 'all':
        df = df[df['month'] == month.title()]

    # filter by day if specified
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]


    return df

def most_common_value(column):
    """
    Returns name and highest count of values from a data frame column

    Args:
        (Series) column - column from dataframe that you wish to run value_counts against
    Returns:
        (tuple) - tuple with name and count from value_counts() result.
    """

    column_value = column.value_counts().index[0]
    count = column.value_counts()[0]

    return column_value, count



def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    monthly_data = most_common_value(df['month'])
    print(f"The most common month was {monthly_data[0]} with {monthly_data[1]} rides.")


    # display the most common day of week
    daily_data = most_common_value(df['day_of_week'])
    print(f"The most common day of the week was {daily_data[0]} with {daily_data[1]} rides.")


    # display the most common start hour
    hourly_data = most_common_value(df['hour'])
    print(f"The most common hour is {hourly_data[0]} with {hourly_data[1]} rides.")    


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    start_station_data = most_common_value(df['Start Station'])
    print(f"The most commonly used start station was {start_station_data[0]} with {start_station_data[1]} rides.")

    # display most commonly used end station
    end_station_data = most_common_value(df['End Station'])
    print(f"The most commonly used end station was {end_station_data[0]} with {end_station_data[1]} rides.")


    # display most frequent combination of start station and end station trip
    most_frequent_trip = df.groupby(['Start Station','End Station']).size().sort_values(ascending=False).index[0]
    most_frequent_count = df.groupby(['Start Station','End Station']).size().sort_values(ascending=False)[0]
    print(f"Most frequent start/end station trip was {most_frequent_trip[0]} to {most_frequent_trip[1]} with {most_frequent_count} rides.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def format_seconds(seconds):
    """ Takes seconds as input and converts to a string with days (if more than one day), hours, minutes and seconds."""
    
    days, remainder = divmod(seconds, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{int(days)} days, {int(hours)} hours, {int(minutes)} minutes, {int(seconds)} seconds."

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print(f"Total travel time is: {format_seconds(total_travel_time)}")


    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print(f"Mean travel time is: {format_seconds(mean_travel_time)}")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_type_counts = df['User Type'].value_counts()
    for user_type, count in user_type_counts.items():
        print(f"Count of {user_type} is {count}.")

    # Display counts of gender
    try:
        gender_counts = df['Gender'].value_counts()
        for gender, count in gender_counts.items():
            print(f"Count of {gender} is {count}.")
    except KeyError:
        print("This datafile does not contain any gender information.")


    # Display earliest, most recent, and most common year of birth
    try:
        birth_filter = df[df['Birth Year'] > 0 ]['Birth Year'] # ignore records with no data
        print(f"Earliest year of birth:  {birth_filter.min()}")
        print(f"Most recent year of birth:  {birth_filter.max()}")
        print(f"Most common year of birth:  {int(birth_filter.mean())}")
    except KeyError:
        print("This datafile does not contain any birth information.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def diplay_raw_data(df):
    """ Prompt user if they want to look at raw data. """
    display = 0

    response = 'yes'
    while response.lower() == 'yes':
        try:
            response = input('Would you like to view the raw data? (yes or no): ')
            if response.lower() == 'yes':
                print(df[display:display+5])
                display += 5
        except KeyboardInterrupt:
            break

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        diplay_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
