from pymongo import MongoClient
import pymongo

def dot_product(a, b):
    return sum([a[i]*b[i] for i in range(len(a))])


def decision( x, w, theta ):
    return (dot_product(x, w) > theta)


def perceptron( training_data ):
    theta = 0
    weights = [ 0 ]
    x = 0
    converged = False
    
    while not converged:
        x += 1
        if x > 50: # Being lazy for now
            converged = True

        for key, val in training_data.iteritems():
            d = decision(key, weights, theta)
            if d == val:
                continue
            elif d == False and val == True:
                theta -= 1
                for i in range(len(key)):
                    weights[i] += key[i]

            elif d == True  and val == False:
                theta += 1
                for i in range(len(key)):
                    weights[i] -= key[i]
        print weights, theta

    return weights, theta

db = MongoClient().test_database



training_data = {
        
}

for data in db.train_data.find():
    training_data[tuple(data["values"])] = data["count"]
    

weights, theta = perceptron( training_data )

print "Done!"

tests = {
        
}

for key, val in tests.iteritems():
    d = decision(key, weights, theta)
    answer = "WRONG"
    if d == val:
        answer = "Correct!"
    print answer, key, d, val