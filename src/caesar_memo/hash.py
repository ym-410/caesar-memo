# パスワードを受け取り、シフト数に変換
def input_password_shift():
      password = input("パスワード：")
      if password == "":
           print("パスワードを入力してください")
           return
      hash_text = sha256(password.encode("utf-8"))
      number = int(hash_text, 16)
      return number % 26

def password_to_shift(password):
    hash_text = sha256(password.encode("utf-8"))
    number = int(hash_text, 16)
    return number % 26

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
    if mod >= size - 8:
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
