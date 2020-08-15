
def read_input(file_name):
    with open(file_name, 'r') as f:
        lines = f.readlines()
        return [line.split() for line in lines]   

def find_count_items(transactions):
    count_items = {}
    for basket in transactions:
        for i in basket:
            if i in count_items.keys():
                count_items[i] += 1
            else:
                count_items[i] = 1
    return count_items
    
def find_frequent_items(count_items, s):
    #frequent_items = dict([(k, v) for k, v in count_items.values() if v >= s])  ko chay duoc
    frequent_items = {}
    for i in count_items.keys():
        if count_items[i] >= s:
            frequent_items[i] = count_items[i]   
    return frequent_items
   
def find_baskets_frequent_item_appear(frequent_items, baskets):
    
    baskets_frequent_item_appear = {}
    numb_basket = 0
    for basket in baskets:
        numb_basket += 1
        for i in basket:
            if i in frequent_items.keys():
                if i not in baskets_frequent_item_appear:
                    baskets_frequent_item_appear[i] = []
                    baskets_frequent_item_appear[i].append(numb_basket)
                else:
                    baskets_frequent_item_appear[i].append(numb_basket)
                    
    return baskets_frequent_item_appear

def find_same_basket(baskets_frequent_items_appear, s):
    same_basket = []
    for i in baskets_frequent_items_appear.keys():
        for j in baskets_frequent_items_appear.keys():
            if i < j:
                a = len( set(baskets_frequent_items_appear[i])&set(baskets_frequent_items_appear[j]))
                if a >= s:
                    same_basket.append([i,j,a])
    return same_basket

def find_association_rules_2(same_basket, frequent_items):
    association_rules =[]
    for x_y_same in same_basket:
        x = x_y_same[0]
        y = x_y_same[1]
        same = x_y_same[2]
        confidence_x_y = same/frequent_items[x]
        confidence_y_x = same/frequent_items[y]
        association_rules.append([x,y,confidence_x_y])
        association_rules.append([y,x,confidence_y_x])
    association_rules.sort(key = lambda x: x[2], reverse=True)
    return association_rules
        
def find_C3(same_basket):
    c_i = {}
    c3 = {}
    for items in same_basket:
        if items[0] not in c_i:
            c_i[items[0]] = 1
        else:
            c_i[items[0]] += 1
        if items[1] not in c_i:
            c_i[items[1]] = 1
        else:
            c_i[items[1]] += 1
    for i in c_i.keys():
        if c_i[i] >= 2:
            c3[i] = c_i[i]
    return c3        
def find_association_rules_3(c3, frequent_items, baskets_frequent_items_appear, s):
    l3 = []
    association_rules_3 = []
    for i in c3.keys():
        for j in c3.keys():
            if i < j:
                for k in c3.keys():
                    if j < k:
                        same = len(set(baskets_frequent_items_appear[i])&set(baskets_frequent_items_appear[j])&set(baskets_frequent_items_appear[k]))
                        if same >= s:
                            l3.append([i,j,k,same])
    for items in l3:
        x = items[0]
        y = items[1]
        z = items[2]
        same = items[3]
        confidence_x_y_z = same/frequent_items[z]
        confidence_x_z_y = same/frequent_items[y]
        confidence_y_z_x = same/frequent_items[x]
        association_rules_3.append([x,y,z,confidence_x_y_z])
        association_rules_3.append([x,z,y,confidence_x_z_y])
        association_rules_3.append([y,z,x,confidence_y_z_x])
    association_rules_3.sort(key = lambda x: x[3], reverse = True)
    return association_rules_3

def save_result(save_file, association_rules_2, association_rules_3):
    with open(save_file,'w') as f:
        for items in association_rules_2:#ket qua cua phan 1
            f.write(items[0] + '->' + items[1] +': ' + str(items[2]) + '\n')  
        f.write('\n'+'Top 5 Association rules: ' + '\n')
        count = 0
        for items in association_rules_2:
            if count < 5:
                f.write(items[0] + '->' + items[1] + '\n')
                count += 1
            else:
                break
        f.write('\n')
        for items in association_rules_3:#ket qua cua phan 2
            f.write('(' + items[0] + ',' + items[1] + ') -> ' + items[2] + ': ' + str(items[3]) + '\n')
        f.write('\n'+'Top 5 Association rules: ' + '\n')
        count = 0
        for items in association_rules_3:
            if(count < 5):
                f.write('(' + items[0] + ',' + items[1] + ') -> ' + items[2] + '\n')
                count += 1
            else:
                break

if __name__ == '__main__':
    inputss = [['a','b'],['a','c','d'], ['a','b'],['a','c','e'],['c','d','e'],['c','d','b','f'],['c','a','d'],['q','o','c','d']]
    s = 100
    
    inputs = read_input('browsing.txt')
    count_items = find_count_items(inputs)
    frequent_items = find_frequent_items(count_items, s)
    baskets_frequent_items_appear = find_baskets_frequent_item_appear(frequent_items, inputs)
    same_basket = find_same_basket(baskets_frequent_items_appear, s)
    association_rules_2 = find_association_rules_2(same_basket, frequent_items)
    c3 = find_C3(same_basket)
    association_rules_3 = find_association_rules_3(c3, frequent_items, baskets_frequent_items_appear, s)
    save_result('output.txt', association_rules_2,association_rules_3)
    