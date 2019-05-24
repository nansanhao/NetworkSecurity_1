# tkinter用于图形界面
import tkinter as tk
import tkinter.messagebox

# 加密的库
import base64
from Crypto.Cipher import AES

# str不是16的倍数那就补足为16的倍数
def add_to_16(text):
    while len(text) % 16 != 0:
        text += '\0'
    return str.encode(text)  # 返回bytes

# 加密按钮回调
def encrypt():
    k = key.get()
    t = text.get()
    # 初始化加密器
    aes = AES.new(add_to_16(k), AES.MODE_ECB)  
    # 加密
    encrypted_t = str(base64.encodebytes(aes.encrypt(add_to_16(t))), encoding='utf8').replace('\n', '') 
    encrypted_text.delete('1.0','end')
    encrypted_text.insert('end',encrypted_t)
    
# 解密按钮回调
def decrypt():
    k = key.get()
    # 初始化加密器
    aes = AES.new(add_to_16(k), AES.MODE_ECB)
    # 解密
    encrypted_t=encrypted_text.get(1.0,'end')
    decrypted_t = str(aes.decrypt(base64.decodebytes(bytes(encrypted_t, encoding='utf8'))).rstrip(b'\0').decode("utf8"))  
    decrypted_text.delete('1.0','end')
    decrypted_text.insert('end',decrypted_t)

if __name__=='__main__':
    # 初始化窗口
    window = tk.Tk()
    window.title('AES加密解密字符串')
    window.geometry("400x160")

    # 绘制界面
    # text输入框
    label = tk.Label(text = '加密内容：',font="Helvetica 10 ")
    label.grid(row=1,column=0)
    text = tk.Entry(window,width=40,font="Helvetica 10 ")
    text.grid(row=1,column=1,sticky='w',padx=5, pady=5)
    # key输入框
    label = tk.Label(text = '密钥：',font="Helvetica 10 ")
    label.grid(row=0,column=0)
    key = tk.Entry(window,width=40,font="Helvetica 10 ")
    key.grid(row=0,column=1,sticky='w',padx=5, pady=5)
    # 加密按钮
    b1 = tk.Button(window,text="加密",command=encrypt,font="Helvetica 10 ",width=10)
    b1.grid(row=2,column=0,sticky='n',padx=5, pady=5)
    # 加密结果
    encrypted_text = tk.Text(window,height=2,width=40,font="Helvetica 10 ")
    encrypted_text.grid(row=2,column=1,sticky='w',padx=5, pady=5)
    # 解密按钮
    b2 = tk.Button(window,text="解密",command=decrypt,font="Helvetica 10 ",width=10)
    b2.grid(row=3,column=0,sticky='n',padx=5, pady=5)
    # 解密结果
    decrypted_text = tk.Text(window,height=2,width=40,font="Helvetica 10 ")
    decrypted_text.grid(row=3,column=1,sticky='w',padx=5, pady=5)

    # 显示出来
    window.mainloop()
    