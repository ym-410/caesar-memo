# パスワードを受け取り、シフト数に変換
def input_password_shift():
      password = input("パスワード：")
      if password == "":
           print("パスワードを入力してください")
           return
      hash_text = sha256(password.encode("utf-8"))
      number = int(hash_text, 16)
      return number % 26
# Base64変換テーブル
TBL = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'

# バイナリデータをBase64に変換する関数 --- (*2)
def base64_encode(bin_data):
    bin = to_binstr(bin_data) # バイナリデータを2進数文字列に変換 --- (*3)
    if len(bin) % 6 >= 1:
        bin += '0' * (6 - len(bin) % 6) # 6ビットに足りない場合0で補完 --- (*4)
    result = ''
    # 6ビットずつに分けて処理 --- (*5)
    for i in range(len(bin) // 6):
        bit6 = bin[i*6:i*6+6]
        result += TBL[bin_to_dec(bit6)] # 変換テーブルから1文字得る --- (*6)
    if len(result) % 4 >= 1:
        result += '=' * (4 - len(result) % 4) # 4の倍数文字数に揃える --- (*7)
    return result

# データを2進数に変換する --- (*8)
def to_binstr(data):
    result = ''
    for b in data: # 1バイトずつ処理
        bin = ''
        for i in range(8): # 8bitずつ処理
            bin = ('1' if (b >> i) & 1 else '0') + bin
        result += bin
    return result

# 2進数を10進数に変換 --- (*9)
def bin_to_dec(bin_str):
    result = 0
    for c in bin_str:
        result <<= 1
        result += 1 if c == '1' else 0
    return result

# Base64デコード --- (*2)
def base64_decode(encoded_str):
    res_bytes = bytearray()
    # TBLを逆引きするための辞書を作成 --- (*3)
    tbl_dict = {}
    for i, c in enumerate(TBL):
        tbl_dict[c] = i
    tbl_dict['='] = 0
    # 4文字ずつ処理 --- (*4)
    for i in range(0, len(encoded_str), 4):
        # 4文字(24ビット)を1つの整数に変換 --- (*5)
        s4 = encoded_str[i:i+4]
        v = 0
        for c in s4:
            v <<= 6
            v += tbl_dict[c]
        # 3バイトに分解 --- (*6)
        res_bytes.append((v >> 16) & 0xff)
        if s4[2] != '=':
            res_bytes.append((v >> 8) & 0xff)
        if s4[3] != '=':
           res_bytes.append((v >> 0) & 0xff)
    return res_bytes



# 暗号化
def encrypt(src, key_no):
    result = ""
    # 1文字ずつ処理する
    for c in src:
        # 大文字ならkey_no分ずらす
        if "A" <= c <= "Z":
            ci = ord(c) # 文字を文字コードに変換
            base = ord("A") # "A"の文字コードを取得
            ci = (ci - base + key_no) % 26 + base
            c = chr(ci) # 文字コードを文字に変換
        elif "a" <= c <= "z":
            base = ord("a")
            c = chr((ord(c) - base + key_no) % 26 + base)
        # 変換結果を追加
        result += c
    return result

# 復号化
def decrypt(src, key_no):
    return encrypt(src, key_no * -1)


# ハッシュの初期値を設定 --- (*1)
SHA256H = [
    0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a,
    0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19]
# 丸め定数を初期化 --- (*2)
SHA256K = [
    0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5,
    0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
    0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3,
    0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
    0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc,
    0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
    0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7,
    0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
    0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13,
    0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
    0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3,
    0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
    0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5,
    0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
    0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208,
    0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2]

# SHA-256のハッシュを求める関数 --- (*1)
def sha256(msg):
    # ハッシュを初期化する --- (*2)
    hi = [SHA256H[i] for i in range(8)]
    # ブロックサイズに合うようにパディング --- (*3)
    msg = bytearray(msg)
    pad = padding(msg, 64)
    # ブロックサイズで区切って繰り返し処理する --- (*4)
    msg_blocks = split_bytes(pad, 64)
    for block in msg_blocks:
        sha256_block(block, hi)
    # HEX文字列で出力
    return ''.join(map(r'{:08x}'.format, hi))

# ビットローテーションを行う --- (*5)
def rotr(x, y):
    return ((x >> y) | (x << (32 - y))) & 0xFFFFFFFF

# 64ビットのブロックを処理 --- (*6)
def sha256_block(block, hi):
    # 64バイトを32ビットずつ16個のリストに分割 --- (*7)
    w = []
    for i in range(16):
        v = (block[i*4+0] << 24) + (block[i*4+1] << 16) + \
            (block[i*4+2] << 8)  + (block[i*4+3])
        w.append(v)
    # 続く16から63バイトまでをローテーション計算
    for i in range(16, 64):
        s0 = rotr(w[i-15], 7) ^ rotr(w[i-15], 18) ^ (w[i-15] >> 3)
        s1 = rotr(w[i-2], 17) ^ rotr(w[i-2], 19) ^ (w[i-2] >> 10)
        w.append((w[i-16] + s0 + w[i -7] + s1) & 0xFFFFFFFF)
    # 変数をハッシュで初期化 --- (*8)
    a,b,c,d,e,f,g,h = [hi[i] for i in range(8)]
    # ローテーション処理
    for i in range(64):
        s0 = rotr(a, 2) ^ rotr(a, 13) ^ rotr(a, 22)
        maj = (a & b) ^ (a & c) ^ (b & c)
        temp2 = s0 + maj
        s1 = rotr(e, 6) ^ rotr(e, 11) ^ rotr(e, 25)
        ch = (e & f) ^ ((~e) & g)
        temp1 = h + s1 + ch + SHA256K[i] + w[i]
        h, g, f = g, f, e
        e = (d + temp1) & 0xFFFFFFFF
        d, c, b = c, b, a
        a = (temp1 + temp2) & 0xFFFFFFFF
    # ハッシュの値を更新
    h2 = (a,b,c,d,e,f,g,h)
    for i in range(8):
        hi[i] = (hi[i] + h2[i]) & 0xFFFFFFFF
# データを指定サイズに合うように詰め物をする --- (*9)
def padding(msg, size):
    bits, mod = (len(msg) * 8, len(msg) % size)
    padcount = size - mod
    if mod > size - 8:
        padcount += 64
    for i in range(padcount):
        msg.append(0x80 if i == 0 else 0)
    # 最後の8バイトは入力のビット数を指定
    for i in range(1, 8+1):
        msg[len(msg) - i] = bits & 0xFF
        bits >>= 8
    return msg

# データを指定バイトごとに区切る --- (*10)
def split_bytes(msg, size):
    a = []
    n = len(msg) // size + (0 if len(msg) % size == 0 else 1)
    for i in range(n):
        a.append(msg[i*size:(i+1)*size])
    return a
