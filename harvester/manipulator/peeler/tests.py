from django.test import TestCase

# Create your tests here.


def cal(candi, target, res, comb, begin):
    print(target, res, comb, begin)
    if not target:
        res.append(comb)
        return
    while begin != len(candi) and target > candi[begin]:
        comb.append(begin)
        cal(candi, target - candi[begin], res, comb, begin)
        comb = []
        begin += 1


def combinationSum(candidates, target):
    """
    :type candidates: List[int]
    :type target: int
    :rtype: List[List[int]]
    """
    c = sorted(candidates)
    res, comb = [], []
    cal(c, target, res, comb, 0)


if __name__ == '__main__':
    combinationSum([2, 2, 3, 6, 7], 7)
