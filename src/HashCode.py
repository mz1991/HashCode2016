import common as CM
import math
import operator
import copy

#lines = CM.read_line("redundancy.in")
#lines = CM.read_line("busy_day.in")
lines = CM.read_line("mother_of_all_warehouses.in")

splitted = lines[0].strip().split()

NUMBER_ROWS = splitted[0]
NUMBER_COLUMNS = splitted[1]
NUMBER_DRONE = splitted[2]
NUMBER_SIMULATION = splitted[3]
NUMBER_MAX_LOAD = splitted[4]

NUMER_DIFFERENT_PRODUCTS = lines[1]

product_weight_line = lines[2]

PRODUCT_WEIGHT = {}

index =0
for wght in product_weight_line.split():
    PRODUCT_WEIGHT[index]=wght
    index = index+1

NUMBER_WAREHOUSE = lines[3]

class Warehouse:
    def __init__(self,row,col,product):
        self.row = row
        self.col = col
        self.product = product

class Order:
    def __init__(self,row,col,product):
        self.row = row
        self.col = col
        self.product = product
        self.distance_warehouses = None


WAREHOUSE_MAP ={}
current_line = 4
for el in range(0,int(NUMBER_WAREHOUSE)):
    row = lines[current_line].split()[0]
    col = lines[current_line].split()[1]
    prod = lines[current_line+1].split()
    wh = Warehouse(row,col,prod)
    WAREHOUSE_MAP[el] = wh
    current_line = current_line+2


NUMBER_ORDERS = lines[current_line]
current_line=current_line+1
ORDER_MAP ={}
for el in range(0,int(NUMBER_ORDERS)):
    row = lines[current_line].split()[0]
    col = lines[current_line].split()[1]
    prod_index = lines[current_line+2].split()
    ord = Order(row,col,prod_index)
    ORDER_MAP[el] = ord
    current_line = current_line+3

def compute_distance(x,x_one,y,y_one):
    return math.floor(math.sqrt(abs(math.pow((int(x)-int(x_one)),2)) + abs(math.pow((int(y)-int(y_one)),2))))+1

def numeric_compare(x):
    return x["distance"]

for order_id in ORDER_MAP:
    order = ORDER_MAP[order_id]
    #distance from all the warehouses
    order_row = order.row
    order_col = order.col
    ordered_wh = []
    for wh_key in WAREHOUSE_MAP:
        wh_value = WAREHOUSE_MAP[wh_key]
        #distance
        distance = compute_distance(int(order_row),int(wh_value.row),int(order_col),int(wh_value.col))
        is_present = False
        for pr in order.product:
            product = int(pr)
            
            #new line
            if int(wh_value.product[product]) > 0:
                ordered_wh.append({"wh_id":wh_key,"distance":distance})

    ordered_wh.sort(key=numeric_compare)

    seen = set()
    unique = []
    for obj in ordered_wh:
        if obj["wh_id"] not in seen:
            unique.append(obj)
            seen.add(obj["wh_id"])

    order.distance_warehouses = unique


dr = 0
def empty_print(load_list,delivery_list):
    for x in load_list:
        print(x)
    for y in delivery_list:
        print(y)
    load_list.clear()
    delivery_list.clear()

load_list =[]
delivery_list =[]

for order_id in ORDER_MAP:

    #print(sum([int(x) for x in WAREHOUSE_MAP[4].product]))

    order = ORDER_MAP[order_id]
    index_prod = 0
    index_wh = 0
    while len(order.product)>0:
        product = order.product[index_prod]
        wh_id = order.distance_warehouses[index_wh]["wh_id"]
        wh = WAREHOUSE_MAP[wh_id]

        loaded_weight = 0

        for p in range(0,len(order.product)):

            product = order.product[p]
            old_qty = wh.product[int(product)]

            if int(old_qty) != 0:
                wh.product[int(product)] = int(old_qty)-1
                
                #order.product[p] = -1
                order.product[p] = ""
                
                tmp_load = str(dr) + " L " + str(wh_id) + " " + str(int(product))  + " 1"
                tmp_delivery = str(dr) + " D " + str(order_id) + " " + str(int(product)) + " 1"

                loaded_weight = int(loaded_weight) + int(PRODUCT_WEIGHT[int(product)])
                if loaded_weight > int(NUMBER_MAX_LOAD):
                    empty_print(load_list,delivery_list)

                load_list.append(tmp_load)
                delivery_list.append(tmp_delivery)
          

        empty_print(load_list,delivery_list)

        #order.product  = [x for x in order.product if x>=0]
        order.product  = [x for x in order.product if len(x)>0]
        index_wh = index_wh+1
        
    dr = dr+1
    dr = dr % int(NUMBER_DRONE)
