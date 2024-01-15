import numpy as np
from random import choices
from collections import Counter



class Matrix():

    def __init__(self, l1, proba_dict=None, m_matrix=None, states=None):
        self.m_matrix= m_matrix
        self.proba_dict = proba_dict
        self.states = states
        self.gen_prob_dict(l1)
        self.create_matrix()


    def create_matrix(self):
        """ Создание самой матрицы, преобразует словарь с вероятностями переходов в матрицу переходов
        """
        di = self.proba_dict
        key_list = sorted(di.keys())
        self.m_matrix = np.array([list(di[i].values()) for i in key_list])





    def gen_prob_dict(self, l1):
        """
        Получает из последовательнности l1(список) двумерный словарь переходов
        поидее можно через Counter сделать, но мне влом
        Даже не буду пытаться описать алгоритм, я уже толком не помню как он работает
        """
        d1 = {}
        d2 = Counter(l1)
        for i, el in enumerate(l1[:-1]):
            if el not in d1.keys():
                d1[el] = []
            d1[el].append(l1[i + 1])

        if l1[-1] not in d1.keys():
            # затычка, надо переделать чтоб выбирался элемент с наибольшей вероятностью
            d1[l1[-1]] = d1[max(d2, key=d2.get)]

        keys_list = sorted(list(set(l1)))
        self.states = keys_list
        for j in d1.keys():
            d1[j] = self.prob(d1[j])
            for k in keys_list:
                if k not in d1[j].keys():
                    d1[j][k] = 0

        for a in d1.keys():
            a_keys = sorted(list(d1[a].keys()))
            d1[a] = {i: d1[a][i] for i in a_keys}

        self.proba_dict = d1

        return self

    @staticmethod
    def prob(l1):
        """
        Вспомогательная функция получения вероятности переходов для каждого элемента в другие элементы
        """
        d1 = {}
        d2 = {}
        for i in l1:
            if i not in d1.keys():
                d1[i] = 1
            else:
                d1[i] += 1

        for key in d1.keys():
            d2[key] = d1[key] / len(l1)

        return d2

    def generate_next(self, starting, n_it):
        """ Генериует следующие члены последовательности на основе имеющейся матрицы переходов
        """
        i = 0
        prev_d = starting
        pred = []
        while i < n_it:
            digit = choices(
                list(self.proba_dict[starting].keys()),
                weights=list(self.proba_dict[starting].values())
            )
            pred.append(digit[0])
            i += 1

        return pred
