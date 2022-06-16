import pickle

import pandas
from sklearn.neural_network import MLPClassifier, MLPRegressor
import numpy as np

import simulator


def main():


    SYMBOLS = ["AMD", "AAPL", "F", "PLTR", "BAC", "SQ", "ZNGA", "NIO", "OPEN", "NVDA", "ITUB", "SOFI", "T", "AAL",
               "VALE",
               "SWN", "INTC", "NOK", "FL", "FB", "PBR", "BBD", "AMC", "ABEV", "CCL", "RPG", "APA"]

    for sym in SYMBOLS:
        # print(f'Training {sym}')
        # clf = MLPClassifier()  # MLPRegressor or MLPClassifier
        # X = []
        # y = []
        # for year in ['2018', '2019', '2020']:
        #     try:
        #         bars = pandas.read_csv('./modified_bars/bars_' + sym + '_' + year + '.csv')
        #     except:
        #         continue
        #     if len(bars) == 0:
        #         continue
        #     # print(bars)
        #     bars = bars.drop(columns=["timestamp"])
        #     bars.reset_index()
        #     for index, rows in bars.iterrows():
        #         if index < len(bars) - 1:  # don't include last one
        #             # print(np.array(rows))
        #             X.append(np.array(rows))
        #
        #     for i in range(len(bars) - 1):
        #         # _y = bars['close'][i + 1] > bars['close'][i]
        #         _y = bars.loc[i+1, 'close'] > bars.loc[i, 'close']
        #         y.append(_y)
        #
        # # print(X)
        # X = np.array(X)
        # y = np.array(y)
        # if len(X) == 0 or len(X) != len(y):
        #     print("skipping " + sym)
        #     continue
        # clf.fit(X, y)
        # pickle.dump(clf, open("./classifiers_1/clf_" + sym + "_1.sav", "wb"))
        # print('Created clf_' + sym + '_1.sav')

        print('starting')
        try:
            clf = pickle.load(open("./classifiers_1/clf_" + sym + "_1.sav", "rb"))
            print("loaded 'clf_" + sym + "_1.sav'")
        except:
            print("skipping " + sym)
            continue
        test_bars = pandas.read_csv('./modified_bars/bars_' + sym + '_2021.csv')
        test_bars = test_bars.drop(columns=["timestamp"])
        test_bars.reset_index()
        results = []
        for index, rows in test_bars.iterrows():
            if index < len(test_bars) - 1:
                result = clf.predict([np.array(rows)])
                results.append(result[0])
        actual = []
        for i in range(len(test_bars) - 1):
            _actual = test_bars['close'][i + 1] > test_bars['close'][i]
            actual.append(_actual)
        correct = 0
        incorrect = 0
        trues = 0
        falses = 0
        for i in range(len(results)):
            if results[i]:
                trues += 1
            else:
                falses += 1

            output = results[i] == actual[i]
            if output:
                correct += 1
            else:
                incorrect += 1
            # print(output)
        print("Results for " + sym)
        print("Trues: " + str(trues))
        print("Falses: " + str(falses))
        print("correct: " + str(correct))
        print("incorrect: " + str(incorrect))
        print(str(100 * correct / (correct + incorrect)) + "%")
        simulator.simulate_trades(test_bars.iloc[:-1, :], results)
        print("----------------------------------")







if __name__ == '__main__':
    main()