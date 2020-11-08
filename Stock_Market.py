# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import os.path as path
import yfinance as yf 

FILE_NAME = "portfolio.txt"

def getCurrentPortfolio():
    file_exists = path.isfile(FILE_NAME)
    
    stocks = {}
    # {"GOOG": 2, "AAPL": 3, "FACEBOOK": 2}
    if file_exists == False:
        balance = 100000
    else:
        port_file = open(FILE_NAME, 'r')
        for line in port_file:
            line_array = line.split()
            if line_array[0] == "balance:":
                balance = float(line_array[1])
            
            if line_array[0] == "stocks:":
                for i in range(1, len(line_array)):
                    stock = line_array[i]
                    
                    stock_data = stock.split(',')
                    ticker = stock_data[0]
                    num_shares = int(stock_data[1])
                    
                    stocks[ticker] = num_shares
        
        port_file.close()
    
    return balance, stocks

def saveCurrentPortfolio(balance, stocks):
    port_file = open(FILE_NAME, 'w+')
    port_file.write("balance: " + str(balance) + '\n')
    port_file.write("stocks: ")
    
    for key in stocks.keys():
        num_shares = stocks[key]
        port_file.write(key + "," + str(num_shares) + " ")
        
        
    
    port_file.close()
    
    
def buyStock(ticker, num_shares):
    balance, stocks = getCurrentPortfolio()
    stock_wanted = yf.Ticker(ticker)
    current_price = stock_wanted.history(period="5d")["Close"][-1]
    
    total_cost = current_price * num_shares
    if total_cost > balance:
        print("Sorry you do not have enough money! ")
        money_needed = total_cost - balance
        print("You need $" + str(money_needed) + " more")
        return balance, stocks
    
    balance -= total_cost
    if ticker in stocks:
        stocks[ticker] += num_shares
    else:
        stocks[ticker] = num_shares
    
    return balance, stocks 

def sellStock(ticker, num_shares_to_sell): 
    balance, stocks = getCurrentPortfolio()
    stock_to_sell = yf.Ticker(ticker) 
    current_price = stock_to_sell.history(period='5d')["Close"][-1] 
    current_profit = num_shares_to_sell * current_price 
    
    if ticker not in stocks: 
        print("Sorry, you don't own any shares of that stock")
        
    if num_shares_to_sell > num_shares: 
        print("Sorry, you do not have enough stock in that company!") 
        stocks_needed = num_shares - num_shares_to_sell 
        print("You need " + str(stocks_needed) + "more! ") 
    else: 
        stocks[ticker] -= num_shares_to_sell 
        balance += current_profit 
        
    return balance, stocks 

def showValue(balance, stocks): 
    total_value = 0 
    for key in stocks.keys(): 
        stock = yf.Ticker(ticker) 
        current_price = stock.history(period='5d')["Close"][-1] 
        stock_value = current_price * stocks[key] 
        total_value += stock_value 
    
    total_assets = total_value + balance 
    return total_value, total_assets 

balance, stocks = getCurrentPortfolio()

while True:
    user_input = input("What would you like to do (Buy/Sell/Show/Quit/Value) ")
    user_input = user_input.lower()
    if user_input == "quit":
        saveCurrentPortfolio(balance, stocks)
        break
    elif user_input == "buy":
        ticker = input("Enter in what stock you want: " ) 
        num_shares = int(input("Enter how many shares: " ))
        balance, stocks = buyStock(ticker, num_shares) 
        saveCurrentPortfolio(balance, stocks) 
        
    elif user_input == "sell":
        ticker = input("Enter in what stock you want to sell: ")
        num_shares = int(input("Enter in how many shares you want to sell: ")) 
        balance, stocks = sellStock(ticker, num_shares) 
        saveCurrentPortfolio(balance, stocks) 
    elif user_input == "show":
        print("Your current balance is $" + str(balance))
        print("Your current stocks: " + str(stocks))
    elif user_input == "value": 
        total_value, total_assets = showValue(balance, stocks)
        print("The current value of your stocks are: $" + str(total_value)) 
        print("The value of your total assets in this account are: $" + str(total_assets)) 
    else:
        print("Choose a valid instruction!")
        
def showPortfolioHistory(ticker, numshares): 
    