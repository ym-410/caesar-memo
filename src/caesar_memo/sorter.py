# resultsをスコアの降順にする
def merge_sort_by_score(results):
    # 要素が1以下ならそのまま返す
    if len(results) <= 1:
        return results

    # 半分に分ける
    center = len(results) // 2
    # 再帰的に分割
    left = merge_sort_by_score(results[:center])
    right = merge_sort_by_score(results[center:])

    return merge_by_score(left, right)

# ソート済みの二つのリストを1つのソート済みリストに合体する
def merge_by_score(left, right):
    result = []
    left_i = 0
    right_i = 0

    while left_i < len(left) and right_i < len(right):
        if left[left_i]["score"] >= right[right_i]["score"]:
            result.append(left[left_i])
            left_i += 1
        else:
            result.append(right[right_i])
            right_i += 1

    if left_i < len(left):
        result.extend(left[left_i:])

    if right_i < len(right):
        result.extend(right[right_i:])

    return result
