# 中文输出
import io
import sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')
# 加密的库
import base64
from Crypto.Cipher import AES
 
 
# str不是16的倍数那就补足为16的倍数
def add_to_16(text):
    while len(text) % 16 != 0:
        text += '\0'
    return str.encode(text)  # 返回bytes
 
# 密钥 
key = '123456'  
# 待加密文本
text = 'abc123def456' 
# 初始化加密器
aes = AES.new(add_to_16(key), AES.MODE_ECB)  
# 加密
encrypted_text = str(base64.encodebytes(aes.encrypt(add_to_16(text))), encoding='utf8').replace('\n', '')  
# 解密
text_decrypted = str(aes.decrypt(base64.decodebytes(bytes(encrypted_text, encoding='utf8'))).rstrip(b'\0').decode("utf8"))  
# 输出结果
print('加密值：', encrypted_text)
print('解密值：', text_decrypted)