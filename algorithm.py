import ast
import datetime as dt
import logging

import numpy as np
import pandas as pd


def tracking_error(weights: np.array, asset_price, option_price, delta):

    # print(f"Asset Price: {asset_price}")
    # print(f"Option Price: {option_price}")
    # print(f"weight0: {weights[0]}, weights[1]: {weights[1]/100}")

    portfolio = weights[0] + (weights[1]/100)*asset_price

    err = 100*abs(portfolio - option_price) + abs(delta - weights[1]/100)
    # print(f"Tracking Error: {err}")

    return err

from scipy.optimize import LinearConstraint, minimize


def optimise(asset_price, option_price, constraints, delta):

    objective_function = tracking_error

    initial_guess = np.random.random(size=2)

    initial_guess[0] *= 430
    initial_guess[1] *= -100
    # print(f"Initial Guess: {initial_guess}")

    args = (asset_price, option_price, delta)

    bounds = [(0, 430), (-100, 0)]
    # print(initial_guess)
    # print("Asset Price: ", asset_price, "Option Price: ", option_price)
    result = minimize(objective_function, x0 = initial_guess ,args = args,
                bounds=bounds, options={'disp': False}, constraints=constraints)

    return result

import json


def replicate(
            asset_price_last_close,
            # option_price_last_close,
            delta,
            verbose = False,
            mode = 'prod'
            ):

        STRIKE = 413.6500
        ENTITLEMENT_RATIO = 97.087

        if (STRIKE - asset_price_last_close) >= 0: option_price_last_close = (STRIKE - asset_price_last_close)
        else: option_price_last_close = 0

        with open("past_weights.txt", 'r') as file:
            previous_weights = ast.literal_eval(file.read())

        most_recent_weights = previous_weights[-1]

        # print(f"Previous Allocation: {previous_weights}")

        past_portfolio_value = most_recent_weights[0] + most_recent_weights[1] * asset_price_last_close
        # print(f"Past Portfolio Value: {past_portfolio_value}")

        self_financing_constraint = LinearConstraint([1, asset_price_last_close/100],
                                    ub = past_portfolio_value, lb = past_portfolio_value)

        weights = optimise(
                        asset_price = asset_price_last_close,
                        option_price = option_price_last_close,
                        constraints = self_financing_constraint,
                        delta = delta
                        # past_weights = previous_weights
                        )['x']

        previous_weights.append([weights[0], weights[1]/100])

        if mode != 'test':

            with open("past_weights.txt", "w") as write_file:
                write_file.write(f"[" + "\n,".join(map(lambda x: str(x), previous_weights))+ "]")

        logging.basicConfig(filename="weights.log", level=logging.INFO)
        logging.info(f"DATE: {dt.datetime.now().strftime('%d-%m-%Y, %H:%M:%S')}| CASH: {round(weights[0], 6)} | ASSET: {round(weights[1]/100, 6)} | OLD PORTFOLIO VALUE: {round(past_portfolio_value, 6)} | NEW PORTFOLIO VALUE: {round(weights[0] + (weights[1]/100) * asset_price_last_close, 6)} | OPTION PRICE: {round(option_price_last_close, 6)}| TRACKING ERROR: {round(past_portfolio_value - option_price_last_close, 6)}")

        if verbose:
            print(f"DATE: {dt.datetime.now().strftime('%d-%m-%Y, %H:%M:%S')}| CASH: {round(weights[0], 6)} | ASSET: {round(weights[1]/100, 6)} | OLD PORTFOLIO VALUE: {round(past_portfolio_value, 6)} | NEW PORTFOLIO VALUE: {round(weights[0] + (weights[1]/100) * asset_price_last_close, 6)} | OPTION PRICE: {round(option_price_last_close, 6)}| TRACKING ERROR: {round(past_portfolio_value - option_price_last_close, 6)}")
