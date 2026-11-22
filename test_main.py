from db import verify_password , hashfunction 

def test_hash_function() :
    ''' This Function Should Take A Normal Password From User And Return A Hashed Password '''
    input_password = 'klmno1234'
    hash_password = hashfunction(input_password)
    assert input_password != hash_password 


def test_same_password_to_hashed ()  :
    ''' IF The Same Password Write Again Should Return Diffrent Values '''
    input_password = 'klmno1234'
    hash_password = hashfunction(input_password)
    hash_password_2 = hashfunction(input_password)
    assert hash_password != hash_password_2 


def test_check_the_strat_of_hash_function() :
    '''This Function Should Return The Real Start Of First 4 Elements In Hashed Password'''
    input_password = 'klmno1234'
    hash_password = hashfunction(input_password)
    assert hash_password[:4] in ('$2a$','$2b$')


def test_check_the_verify_password_function_error () :
    '''This Function Should Check The Input Password Equal The Value OF The Hashed Passwrd In The Data Base (Error Type) '''
    input_passwrd ='12345678'
    hashed =  hashfunction(input_passwrd)
    password_to_check = '1234'
    
    assert verify_password(password_to_check,hashed) is False
  
def test_check_the_verify_password_function_passed () :
    
    '''This Function Should Check The Input Password Equal The Value OF The Hashed Passwrd In The Data Base (Passed Type) '''
    hashed = hashfunction('12345678')
    
    password_to_check_2 ='12345678'
    assert verify_password(password_to_check_2,hashed) is True
 
  