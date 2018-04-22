# string-average

Implementation of fast string averages for strings in Python.
Algorithm description:
(D) https://pdfs.semanticscholar.org/0c64/a383faf7f7af6242dc8842d17045c9ab2591.pdf

(R) The library uses C extension modules for fast computation (dependency)
https://rawgit.com/ztane/python-Levenshtein/master/docs/Levenshtein.html

There are 3 functions available:

1. get_string_average(string_tab)
median of strings, equivalent to median (R)

2. better_average(string_tab, max_iter)
Iterative median of strings. The algorithm starts from the string median (R) and applies pseudo code from (D) to improve teh average

3. get_string_average_prob(mode, string_tab_with_prob, max_iter)
Iterative median of strings with probabilities for every string char. Modification of (2).




