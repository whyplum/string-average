from Levenshtein import *
import collections
import math



def get_string_average(string_tab): 

  #if output is empty, return an empty string
  if len(string_tab)==0:
    return ""

  #covert into strings and remove extra white signs:
  string_tab = [str(s).replace(" ", "") for s in string_tab]

  average = median(string_tab)

  return average




def better_average(string_tab, max_iter):

  #if output is empty, return an empty string
  if len(string_tab)==0:
    return ""

  max_iter = min(max_iter, 100)
  curr_average = median(string_tab)

  #covert into strings and remove extra white signs:
  string_tab = [str(s).replace(" ", "") for s in string_tab]


  def better_average_inner(string_tab, curr_average, curr_iter, max_iter):


    string_tab_len = len(string_tab)

    #calculate edits and modify weights by probabilities
    edits = []
    for s in string_tab:
      edits_item = editops(curr_average, s)
      edits+=([[e, s] for e in edits_item])

    #collect suggested edits for every position in the average string
    pos_edits = []
    for i in range(len(curr_average)):
      pos_edit = [edit for edit in edits if edit[0][1]==i]
      pos_edits.append(pos_edit)

    #change the third argument into the destimation char:
  
    for pos_edit in pos_edits:
      for edit in pos_edit:
        if(edit[0][0]=='delete'):
          edit.append("")
        else:
          edit.append(edit[1][edit[0][2]])  

    #fill with equals
    for i in range(len(pos_edits)):
      if len(pos_edits[i])<string_tab_len:
        for j in range(string_tab_len - len(pos_edits[i])):
          pos_edits[i].append([("equal", i, i), curr_average, curr_average[i]])

    simplified_pos_edits = [[(edit[0][0], edit[2]) for edit in pos_edit] for pos_edit in pos_edits]


    edits_apply = [] 

    #find most common operation for every pos here intruduce probabilities later:
    for i in range(len(simplified_pos_edits)):
      e_col = collections.Counter(simplified_pos_edits[i])
      if len(e_col)>1:
        edit1, edit2 = e_col.most_common(2)
        if edit1[1]>edit2[1] and edit1[0][0]!="equal":
          edits_apply.append([(edit1[0][0], i, 0), curr_average, edit1[0][1]])
        elif len(e_col)>0:
          edit1 = e_col.most_common(1)[0]
          if edit1[0][0]!="equal":
            edits_apply.append([(edit1[0][0], i, 0), curr_average, edit1[0][1]])


    if len(edits_apply)>0:
      curr_average = apply_edit([edits_apply[0][0]], edits_apply[0][1], edits_apply[0][2])
      if(curr_iter<max_iter):
        return better_average_inner(string_tab, curr_average, curr_iter+1, max_iter)
      else: 
        return curr_average
    else:
      return curr_average

  return better_average_inner(string_tab, curr_average, 0, max_iter)




def get_string_average_prob(mode, string_tab_with_prob, max_iter):

  max_iter = min(max_iter, 800)

  #if output is empty, return an empty string
  if len(string_tab_with_prob)==0:
    return ""

  #covert into strings and remove extra white signs:
  string_tab_prob = [[str(s[0]).replace(" ", ""), s[1]] for s in string_tab_with_prob]
  string_tab = [s[0] for s in string_tab_prob]

  #step0: get standard median - candidate for the average
  curr_average = median(string_tab)

  def probability(mode, char1, char2, char2_prob):
    if mode=="conditional":
      return 1
    elif mode=="normal":
      return int(char2_prob/0.05)
    elif mode=="scaled":
      return int(char2_prob**4/0.005)


  def get_string_average_prob_inner(mode, string_tab_prob, curr_average, curr_iter, max_iter):

    string_tab_len = len(string_tab_prob)

    #calculate edits and modify weights by probabilities
    edits = []
    for s in string_tab_prob:
      edits_item = editops(curr_average, s[0])
      edits+=([[e, s] for e in edits_item])

    #collect suggested edits for every position in the source string
    pos_edits = []
    for i in range(len(curr_average)):
      pos_edit = [e for e in edits if e[0][1]==i]
      pos_edits.append(pos_edit)

    #change the third argument into the destination char, append probabilities - source char and destination char:
    #for j in range(len(average)):
    for pos_edit in pos_edits:
      for e in pos_edit:
        if(e[0][0]=='delete'):
          e+=["", probability(mode, curr_average[e[0][1]], "", 0.75)]
        elif len(e)>0:
          e+=[e[1][0][e[0][2]], probability(mode, curr_average[e[0][1]], e[1][0][e[0][2]], e[1][1][e[0][2]])]


    #fill with equals
    for i in range(len(pos_edits)):
      if len(pos_edits[i])<string_tab_len:
        for j in range(string_tab_len - len(pos_edits[i])):
          pos_edits[i].append([("equal", i, i), curr_average, curr_average[i], probability(mode, curr_average[i], curr_average[i], 0.75)])
   

    pos_edits_prob=[]
    #duplicate to represent absolute probabilities:
    for pos_edit in pos_edits:
      pos_edit_repeated = []
      for e in pos_edit:
        repeat = e[3]
        pos_edit_repeated+=[e]*repeat
      pos_edits_prob.append(pos_edit_repeated)

    simplified_pos_edits = [[(e[0][0], e[2]) for e in pos_edit] for pos_edit in pos_edits_prob]

    edits_apply = [] 

    #find most common operation for every pos here intruduce probabilities later:
    for i in range(len(simplified_pos_edits)):
      e_col = collections.Counter(simplified_pos_edits[i]) 
      if len(e_col)>1:
        e1, e2 = e_col.most_common(2)
        if e1[1]>e2[1] and e1[0][0]!="equal":
          edits_apply.append([(e1[0][0], i, 0), curr_average, e1[0][1]])
        elif len(e_col)>0:
          e1 = e_col.most_common(1)[0]
          if e1[0][0]!="equal":
            edits_apply.append([(e1[0][0], i, 0), curr_average, e1[0][1]])


    if len(edits_apply)>0:
      curr_average = apply_edit([edits_apply[0][0]], edits_apply[0][1], edits_apply[0][2])
      if(curr_iter< max_iter):
        return get_string_average_prob_inner(mode, string_tab_prob, curr_average, curr_iter+1, max_iter)
      else:
        return curr_average
    else:
      return curr_average


  return get_string_average_prob_inner(mode, string_tab_prob, curr_average, 0, max_iter)

