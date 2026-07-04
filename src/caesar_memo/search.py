from .sorter import merge_sort_by_score

def ngram(text, n):
    # 文字を小文字にする
    text = text.lower()

    # 文字列の長さが分割しする数より小さい場合はそのままリストに入れる
    if len(text) < n:
        return [text]

    result = []
    # 切り出す数を決定
    nlen = len(text) - n + 1

    # 実際にn文字ずつ切り出す
    for i in range(nlen):
        result.append(text[i:i+n])

    return result

# 2つの文字列aとbの類似度を計算
def calc_similarity(a, b, n):
    a_set = set(ngram(a, n))
    b_set = set(ngram(b, n))

    # どちらが空なら0を返す
    if len(a_set) == 0 or len(b_set) == 0:
        return 0

    # 共通しているn-gramの数を数える
    count = 0

    # a_setの要素がb_setにあれば +1
    for word in a_set:
        if word in b_set:
            count += 1

    # 共通している数 / 大きい方の集合サイズ
    return count / max(len(a_set), len(b_set))


def search_notes(notes, keyword):
    results = [] # 検索結果を入れるリスト

    for note in notes:
        score = calc_similarity(keyword, note["title"], 2)

        if score > 0.2: # 閾値
            results.append({
                "note": note,
                "score": score
            })

    return merge_sort_by_score(results)
