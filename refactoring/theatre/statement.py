from math import floor


def statement(invoice, plays):
    total_amount = 0
    volume_credits = 0
    result = f'Statement for {invoice["customer"]}\n'

    for perf in invoice["performances"]:
        play = plays[perf["playID"]]
        this_amount = 0

        if play["type"] == "tragedy":
            this_amount = 40000
            if perf["audience"] > 30:
                this_amount += 1000 * (perf["audience"] - 30)
        elif play["type"] == "comedy":
            this_amount = 30000
            if perf['audience'] > 20:
                this_amount += 10000 + 500 * (perf["audience"] - 20)
            this_amount += 300 * perf["audience"]
        else:
            raise Exception(f'Unknown type: {play["type"]}')
        # add volume credits
        volume_credits += max(perf['audience'] - 30, 0)
        # add extra credits for every ten comedy attendees
        if 'comedy' == play["type"]:
            volume_credits += floor(perf["audience"]/5)
        result += f'  {play["name"]}: {format_currency(this_amount / 100)} ({perf["audience"]} seats)\n'
        total_amount += this_amount
    result += f'Amount owed is {format_currency(total_amount / 100)}\n'
    result += f'You earned {volume_credits} credits\n'
    return result


def format_currency(value):
    return f'${value:,.2f}'


if __name__ == "__main__":
    import json
    output = statement(
            json.load(open('invoices.json'))[0],
            json.load(open('plays.json')),
        )
    print(output)
