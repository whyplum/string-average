from string_average import *

#standard string average:
#get_string_average(string_tab) 

m0 = get_string_average([1234, "1234k", 12345, "01234"])
print(m0)


#improved string average:
#better_average(string_tab, max_iter)

m1 = better_average(['Kowal' , 'Kowalski', 'alski'], 100)
print(m1)


#string average with probabilities
#get_string_average_prob(mode, string_tab_with_prob, max_iter)

input_with_prob = [[346, [0.95, 0.70, 0.2]], [316, [0.95, 0.9, 0.2]], [1348, [0.5, 0.95, 0.70, 0.8]]]

m2 = get_string_average_prob("scaled", input_with_prob, 100)
print(m2)
