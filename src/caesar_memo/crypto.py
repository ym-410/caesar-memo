# シーザー暗号変換

def shift_range(c, start, end, key_no):
    # 文字をUnicode番号に変換
    code = ord(c)

    # 対象範囲外の場合、そのまま返す
    if not (start <= code <= end):
        return c

    # 範囲の文字数
    size = end - start + 1

    return chr((code - start + key_no) % size + start)


# 暗号化
def encrypt(src, key_no):
    result = ""
    # 1文字ずつ処理する
    for c in src:
        # 大文字ならkey_no分ずらす
        if "A" <= c <= "Z":
            c = shift_range(c, ord("A"), ord("Z"), key_no)
        elif "a" <= c <= "z":
            c = shift_range(c, ord("a"), ord("z"), key_no)
        elif "ぁ" <= c <= "ゖ":
            c = shift_range(c, ord("ぁ"), ord("ゖ"), key_no)
        elif "ァ" <= c <= "ヺ":
            c = shift_range(c, ord("ァ"), ord("ヺ"), key_no)
        elif "一" <= c <= "龯":
            c = shift_range(c, ord("一"), ord("龯"), key_no)

        # 変換結果を追加
        result += c
    return result

# 復号化
def decrypt(src, key_no):
    return encrypt(src, key_no * -1)