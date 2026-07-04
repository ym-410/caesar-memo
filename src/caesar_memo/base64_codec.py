# Base64変換

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