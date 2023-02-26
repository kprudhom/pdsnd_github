import time
import pandas as pd
import numpy as np

CITY_DATA = { 'Chicago': 'chicago.csv',
              'New York City': 'new_york_city.csv',
              'Washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        try:
            check = "" #default value
            city = input("Would you like to explore data from Chicago, New York City or Washington?\n").title() #ask which city
            if city == "Chicago" or city == "New York City" or city == "Washington":
                check = input("You have selected {}. Is that correct Y/N?\n".format(city)).capitalize() #confirming choice
                if check == "Y":
                    break #choice was registered, exit loop
                elif check == "N": #choice not understood - start over
                    print("I'm sorry, I did not understand. Please try again.")
        except: #if an error occurs (any type)
            print("That's not a valid input. Make sure to select either Chicago, New York City or Washington.")
        else:
            if check != "N": #if the entry was not valid: start over.
                print("That's not a valid input. Make sure to select either Chicago, New York City or Washington.")

    # TO DO: get user input for month (all, january, february, ... , june)
    loop_check = True #default value
    months = ["January","February","March","April","May","June"] #Possible months
    while loop_check:
        month = input("Would you like to filter on a month? Y/N\n").capitalize()
        if month == "Y":
            month = input("Which month would you like to filter on?\n").title()
            if month in months:
                print("The results will be filtered on the month of {}.".format(month))
                loop_check = False #exit loop - choice was registered
            else:
                 print("I'm sorry, I did not understand. Please try again.")  #choice not registered: start over
        elif month == "N":
            month = "all"
            loop_check = False #choice was registered - exit loop
        else:
            print("I'm sorry, I did not understand, please try again") #choice not registered: start over

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    loop_check = True #default value
    days = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"] #possible weekdays
    while loop_check:
        day = input("Would you like to filter on a weekday? Y/N\n").capitalize()
        if day == "Y":
            day = input("Which weekday would you like to filter on (please spell it out)?\n").title()
            if day in days:
                print("The results will be filtered on {}.".format(day))
                loop_check = False #exit loop - choice registered
            else: #choice not registered: start over
                 print("I'm sorry, I did not understand. Please try again.")  
        elif day == "N":
            day = "all"
            loop_check = False #exit loop - choice registered
        else: #choice not registered: start over
            print("I'm sorry, I did not understand. Please try again.")
                    
        

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
    ##took this from problem #3
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['January', 'February', 'March', 'April', 'May', 'June']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    #remove problematic birth years and genders
    if city != "Washington":
        df = df[df['Birth Year'] > 1923] #assuming if you are 100 or older, you aren't riding a bike and your birth year is in fact an error.
        df = df[df['Gender'] != ""] #removing blank genders
    
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    months = ["January","February","March","April","May","June"]
    common_month = months[df['month'].mode()[0]-1]
    print("The most common month is: {}.".format(common_month))

    # TO DO: display the most common day of week
    common_day = df['day_of_week'].mode()[0]
    print("The most common day of the week is: {}.".format(common_day))

    # TO DO: display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    common_hour = df['hour'].mode()[0]
    print("The most common start hour (24hr clock) is: {}.".format(common_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    common_start = df['Start Station'].mode()[0]
    print("The most common start station is: {}.".format(common_start))

    # TO DO: display most commonly used end station
    common_end = df['End Station'].mode()[0]
    print("The most common end station is: {}.".format(common_end))

    # TO DO: display most frequent combination of start station and end station trip
    df['Start and end'] = df['Start Station'] + " and " + df['End Station'] #create combination of start and end stations
    common_start_end = df['Start and end'].mode()[0]
    print("The most common start and end stations are: {}.".format(common_start_end))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_duration = df['Trip Duration'].sum()
    print("The total travel time is {} seconds, or {} minutes, or {} hours, or {} days.".format(total_duration, (total_duration/60).round(2), (total_duration/60/60).round(2), (total_duration/60/60/24).round(2)))

    # TO DO: display mean travel time
    common_duration = df['Trip Duration'].mean()
    print("The mean travel time is {} seconds, or {} minutes.".format(common_duration.round(2), (common_duration/60).round(2)))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_counts = df['User Type'].value_counts()
    print("Here are the counts of each user type:\n{}".format(user_counts))

    # TO DO: Display counts of gender
    if city == "Washington":
        print("Gender information is not available for Washington.")
    else:
        gender_counts = df['Gender'].value_counts()
        print("Here are the counts of each gender:\n{}".format(gender_counts))

    # TO DO: Display earliest, most recent, and most common year of birth
    if city == "Washington":
        print("Birth Year information is not available for Washington.")
    else:
        print("Earliest year of birth: {}\nMost recent year of birth: {}\nMost common year of birth: {}".format(int(df['Birth Year'].min()), int(df['Birth Year'].max()), int(df['Birth Year'].mode()[0])))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df):
    """displays raw data from df if the user requests it."""

    loop_check = True
    index = 0

    while loop_check == True:
        raw = input("Would you like to see raw data? Y/N\n").capitalize()    

        if raw == "Y":
            print(df.loc[index + 1 : index + 5,:])
            index += 5
            while loop_check == True:
                again = input("Would you like to see more data? Y/N\n").capitalize()
                if again == "N":
                    loop_check = False
                elif again != "Y":
                    print("I'm sorry, I did not understand. Please try again.")
                else:
                    print(df.loc[index + 1 : index + 5,:])
                    index += 5
        elif raw != "N":
            print("I'm sorry, I did not understand. Please try again.")
        else:
            loop_check = False
            
    
    
def main():
    check_start = True #loop until the user wants to stop
    while check_start == True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        raw_data(df)

        check_restart = True 
        while check_restart == True: #Loop until a valid response is entered
            restart = input('\nWould you like to restart? Enter yes or no.\n')
            if restart.lower() == 'no':   
                check_restart = False
                check_start = False
            elif restart.lower() != 'yes':
                print("That is not a valid response. Please try again.")
            else:
                check_restart = False
            


if __name__ == "__main__":
    main()
