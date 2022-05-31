import math
import random

digits="0123456789"
otp=""
def generate_otp():
    for i in range(4) : 
        OTP += digits[math.floor(random.random() * 10)] 
  
    return OTP 