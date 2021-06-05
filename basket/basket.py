

class Basket():
    def __init__(self, request):
        self.session = request.session
        basket = self.session.get('skey')
        if 'skey' not in self.session:
            basket = self.session['skey'] = {}
        self.basket = basket

    def add(self, recipe, qty):
        recipe_id = recipe.id
        if recipe_id in self.basket:
            self.basket[recipe_id]['qty'] = qty
        else:
            self.basket[recipe_id] = {'price': int(recipe.price), 'qty': qty}
        
        self.session.modified = True

    def __len__(self):
        return sum(item['qty'] for item in self.basket.values())