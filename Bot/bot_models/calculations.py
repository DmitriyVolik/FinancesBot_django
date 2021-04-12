class deposit:

    tax = 19.5

    def calculation_deposit(self, percent_year, amount, term, type_dep):

        percent_year =float(percent_year)

        amount=float(amount)

        term=int(term)

        percent_year = round(percent_year -
                             (percent_year*self.tax/100), 2)

        percent = round(percent_year/12, 2)

        if(type_dep == "on_deposit"):

            total_money = amount

            for i in range(int(term)):
                total_money += total_money*percent/100
            total_money = round(total_money, 2)
            return "💰Ваш підсумковий рахунок:"+str(total_money)+"\n💰У підсумку ви заробите:"+str(round(total_money-(amount), 2))
        else:
            total_money = 0
            for i in range(term):
                total_money += amount*percent/100

            return "💰У підсумку ви заробите:"+str(total_money)
