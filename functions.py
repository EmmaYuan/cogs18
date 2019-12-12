import random 
import string
import pandas as pd


CHOICES = ['cuisine', 'distance', 'rating'] # default choices for the user  

# different conversations based on different user input
IK_OUT = ['Here you go:', 'Look what I have found:', 
          'Here are some options:'] # start
IK_MORE_OUT = ['Here are more factors you can choose from: ', 
               'Got one down! Do you have other preferences: '] # mid
IK_EVERYTHING_OUT = ['Thank you and see you next time!', 
                     'Here is the final result! Enjoy your lunch.'] # end
IDK_OUT = ["Sorry I cannot understand", 
           'Wow you are way too smart. I cannot follow your logic',  
           "Hey can you check if you type in the valid format"]

output = [0, 1, 2, 3, 4, 5] # default dining hall 
chat = True

# menu 
bistro_cs = ['sushi', 'ramen', 'udon']
sf_north_cs = ['ramen', 'linguini', 'risotto']
cv_cs = ['salad', 'grill', 'burger']
ovt_cs = ['pizza', 'bagel', 'salad']
pines_cs = ['grill', 'curry', 'salad']
fw_cs = ['sandwich', 'salad', 'pizza']

# longitude and latitude of each college (/ dining hall) 
# will be computed in check_distance(x, y, z) later  
loc = {'erc' : (33.1967, -117.3862), 'revelle' : (33.2952, -117.3178), 
       'warren' : (32.7956, -117.1782), 'marshall':(33.1959, -117.2352), 
       'miur': (32.9026, -117.2422), 'six': (32.7157, -117.1638)}

# each dining hall has 3 factors: cuisine, distance, and rating 
data = {'Name':['The Bistro at the Strand', 'Sixty-Four North', 
                'Canyon Vista', 'Oceanview Terrace', 'Pines', 'Foodworx'],
        'cuisine': [bistro_cs, sf_north_cs, cv_cs, ovt_cs, pines_cs, fw_cs],
        'distance':[loc['erc'], loc['revelle'], loc['warren'], 
                    loc['marshall'], loc['miur'], loc['six']],
        'rating':[0, 1, 2, 3, 4, 5]}
df = pd.DataFrame(data)

def remove_punctuation(input_string):
    '''Removes punctuations.'''
    out_string = ''
    for hi in input_string:
        if not(hi in string.punctuation):
            out_string += hi
    return out_string

def prepare_text(input_string):
    ''' Lower the letters and removes punctuations.'''
    temp_string = input_string.lower()
    temp_string = remove_punctuation(temp_string)
    return temp_string

def update_cuisine():
    '''Selects the dining halls that have a certain cuisine.'''
    global output
    possible_cs = ""

    # go through all cuisine options from the dining halls on the output list
    for possible_dining_hall in output:
        for single_cs in df.loc[possible_dining_hall, 'cuisine']:
            if single_cs not in possible_cs:
                possible_cs += single_cs + ", "
    possible_cs = possible_cs[:-2] # remove the last comma 
    
    print('Emma:', """Here are some choices! 
          Check out which one you prefer!"""+'\n'+'      '+possible_cs)
    msg = input('User: ')
    temp = [] # store the prefered dining halls temporarily 

    # go through all dining halls on the output list 
    for possible_dining_hall in output:
        for single_cs in df.loc[possible_dining_hall, 'cuisine']:
            if msg == single_cs: 
                temp.append(possible_dining_hall) # select the ones that serve the msg cuisine
    output = temp # update the output

    print('Emma:', random.choice(IK_OUT), print_op())
    CHOICES.remove('cuisine') # remove the option of choosing 'distance' again
    return 'Emma:', random.choice(IK_OUT), print_op()
        
def update_distance():
    '''Sorts the output list from the closest to the furthest.'''
    print('Emma:', 'Cool. Which college are you in right now?')

    # get the user's location  
    msg = input('User: ')
    while msg not in list(loc.keys()):
        print('Emma:', random.choice(IDK_OUT))
        msg = input('User: ')  
    
    # compute the longitude and latitude
    x = 0
    y = 0
    for item in list(loc.keys()):
        if item == msg:
            x = int((loc[item][0] - 33)*100)
            y = int((loc[item][1] + 117)*100)
    
    wall_index = 0 # the wall separates the sorted and the unsorted
    global output

    # go through the unsorted elements on the right of the wall
    for item_1 in output[wall_index:]:    
        min_index = wall_index
        for item_2 in output[wall_index+1:]:
            # compare the distance between each of the two unsorted dining halls and the user
            if(check_distance(df.loc[item_2, 'distance'], x, y) < 
               check_distance(df.loc[min_index, 'distance'], x, y)):
                min_index = item_2
        # swap the two elements in the output list
        temp = output[wall_index]
        output[wall_index] = output[min_index]
        output[min_index] = temp 
        wall_index += 1 # increased by one since there is one dining hall is just sorted

    # delete the last elements based on the current length
    if len(output) > 2:
        output = output[: -2]
    else: 
        output = output[: -1]    

    print('Emma:', random.choice(IK_OUT), print_op())
    CHOICES.remove('distance') # remove the option of choosing 'distance' again
    return 'Emma:', random.choice(IK_OUT), print_op()

def check_distance(coord, x, y):
    '''Returns the distance between a dining hall and the user.'''
    # compute the longitude and latitude
    coord_x = int((coord[0] - 33)*100)
    coord_y = int((coord[1] + 117)*100)

    # apply the distance formula
    delta_x = pow((abs(coord_x) - abs(x)), 2)
    delta_y = pow((abs(coord_y) - abs(y)), 2)
    return pow((delta_x + delta_y), 1/2)    

def update_rating():
    '''Sorts the output list from the best to the worst (based on my opinion).'''
    wall_index = 0 # the wall separates the sorted and the unsorted
    global output

     # go through the unsorted elements on the right of the wall
    for item_1 in output:
        min_index = wall_index
        for item_2 in output[wall_index:]:
            # compare the rating of the two unsorted dining halls
            if(output[item_2] < output[min_index]):
                min_index = item_2
        # swap the two elements in the output list
        temp = output[wall_index]
        output[wall_index] = output[min_index]
        output[min_index] = temp 
        wall_index += 1 # increased by one since there is one dining hall is just sorted
    
    # delete the last elements based on the current length
    if len(output) > 2:
        output = output[: -2]
    else: 
        output = output[: -1]

    print('Emma:', random.choice(IK_OUT), print_op())
    CHOICES.remove('rating') # remove the option of choosing 'rating' again
    return 'Emma:', random.choice(IK_OUT), print_op()

def print_op():
    '''Returns the updated output list.'''
    output_str = ''
    for item in output:
        output_str += df.loc[item, 'Name'] + ", "
    return output_str[:-2]

def check():
    '''Check what to print based on the remaining dining halls.'''
    global chat
    if len(output) <= 1:
        print('     ', random.choice(IK_EVERYTHING_OUT))
        chat = False # conversation ends
    else:
        print('     ', random.choice(IK_MORE_OUT))
        for item in CHOICES:
            print("     ", item)

def have_a_chat():
    '''Main function.'''
    print("""Emma: Hi! My name is Emma.
      I am here to help you decide which dining hall to go for lunch today!
      Which catogory do you focus more: cuisine, distance, or rating?""")
    global chat 
    while chat:
        msg = input('User: ')
        msg = prepare_text(msg)
       
        # call method based on user's input 
        if msg == 'cuisine' and 'cuisine' in CHOICES:
            update_cuisine()
            check()
        elif msg == 'distance' and 'distance' in CHOICES:
            update_distance()
            check()
        elif msg == 'rating' and 'rating' in CHOICES:
            update_rating()
            check()
        else:                 
            print('Emma:', random.choice(IDK_OUT))
have_a_chat()
