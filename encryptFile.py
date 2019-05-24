import os, random, struct
import tkinter as tk
import tkinter.messagebox
import tkinter.filedialog
from Crypto.Cipher import AES
try:
    from Crypto.Util.Padding import pad, unpad
except ImportError:
    from Crypto.Util.py3compat import bchr, bord
    def pad(data_to_pad, block_size):
        padding_len = block_size-len(data_to_pad)%block_size
        padding = bchr(padding_len)*padding_len
        return data_to_pad + padding
    def unpad(padded_data, block_size):
        pdata_len = len(padded_data)
        if pdata_len % block_size:
            raise ValueError("Input data is not padded")
        padding_len = bord(padded_data[-1])
        if padding_len<1 or padding_len>min(block_size, pdata_len):
            raise ValueError("Padding is incorrect.")
        if padded_data[-padding_len:]!=bchr(padding_len)*padding_len:
            raise ValueError("PKCS#7 padding is incorrect.")
        return padded_data[:-padding_len]

# 加密文件
def encrypt_file(key, in_filename, out_filename=None, chunksize=64*1024):
    if not out_filename:
        out_filename = in_filename + '.enc'
    iv = os.urandom(16)
    encryptor = AES.new(key, AES.MODE_CBC, iv)
    filesize = os.path.getsize(in_filename)
    with open(in_filename, 'rb') as infile:
        with open(out_filename, 'wb') as outfile:
            outfile.write(struct.pack('<Q', filesize))
            outfile.write(iv)
            pos = 0
            while pos < filesize:
                chunk = infile.read(chunksize)
                pos += len(chunk)
                if pos == filesize:
                    chunk = pad(chunk, AES.block_size)
                outfile.write(encryptor.encrypt(chunk))

# 解密文件
def decrypt_file(key, in_filename, out_filename=None, chunksize=64*1024):
    if not out_filename:
        out_filename = in_filename + '.dec'
    with open(in_filename, 'rb') as infile:
        filesize = struct.unpack('<Q', infile.read(8))[0]
        iv = infile.read(16)
        encryptor = AES.new(key, AES.MODE_CBC, iv)
        with open(out_filename, 'wb') as outfile:
            encrypted_filesize = os.path.getsize(in_filename)
            pos = 8 + 16 # the filesize and IV.
            while pos < encrypted_filesize:
                chunk = infile.read(chunksize)
                pos += len(chunk)
                chunk = encryptor.decrypt(chunk)
                if pos == encrypted_filesize:
                    chunk = unpad(chunk, AES.block_size)
                outfile.write(chunk) 

# 选择文件按钮回调
def chooseFile():
    default_dir ="C:\\Users\38974\Desktop\Security" # 设置默认打开目录
    fname = tk.filedialog.askopenfilename(title="选择加密文件",initialdir=(os.path.expanduser(default_dir)))
    encryptFile.delete('1.0','end')
    encryptFile.insert('end',fname)

# 加密按钮回调
def encrypt():
    k=add_to_16(key.get())
    if k=="":
        tk.messagebox.showinfo(title='警告', message='密钥不能为空！')
    else: 
        filename=encryptFile.get(1.0,'end').replace('\n','')
        encrypt_file(k.encode('utf-8'),filename)
        tk.messagebox.showinfo(title='成功', message='加密文件成功！')

# 解密按钮回调
def decrypt():
    k=add_to_16(key.get())
    if k=="":
        tk.messagebox.showinfo(title='警告', message='密钥不能为空！')
    else:
        filename=encryptFile.get(1.0,'end').replace('\n','')+'.enc'
        decrypt_file(k.encode('utf-8'),filename)
        tk.messagebox.showinfo(title='成功', message='解密文件成功！')

# str不是16的倍数那就补足为16的倍数
def add_to_16(text):
    while len(text) % 16 != 0:
        text += '\0'
    return text  # 返回bytes

# 居中窗口
def center_window(w, h):
    # 获取屏幕 宽、高
    ws = window.winfo_screenwidth()
    hs = window.winfo_screenheight()
    # 计算 x, y 位置
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)
    window.geometry('%dx%d+%d+%d' % (w, h, x, y))

#主函数
if __name__=='__main__':
    # 初始化窗口
    window = tk.Tk()
    window.title('AES算法CBC模式加密解密文件')
    center_window(350, 280)

    # 绘制界面
    # 加密内容
    label = tk.Label(text = '加密内容：',font="Helvetica 16 bold")
    label.grid(row=0,column=0)
    # 选择文件
    b1 = tk.Button(window,text="选择加密文件",command=chooseFile,font="Helvetica 16 bold",width=11)
    b1.grid(row=0,column=1,padx=5, pady=5)
    encryptFile = tk.Text(window,height=2,width=28,font="Helvetica 16 ")
    encryptFile.grid(row=1,column=0,padx=5, pady=5,columnspan=2)

    # 密钥
    label = tk.Label(text = '加密密钥：',font="Helvetica 16 bold")
    label.grid(row=2,column=0)
    key = tk.Entry(window,width=12,font="Helvetica 16 bold")
    key.grid(row=2,column=1,padx=5, pady=5)

    # 加密选中的文件按钮
    b2 = tk.Button(window,text="加密文件",command=encrypt,font="Helvetica 16 bold",width=11)
    b2.grid(row=3,column=0,padx=5, pady=10)

    # 解密已加密的文件按钮
    b2 = tk.Button(window,text="解密文件",command=decrypt,font="Helvetica 16 bold",width=11)
    b2.grid(row=3,column=1,padx=5, pady=10)

    # 注
    labelNotice = tk.Label(text = '注：加密和解密生成的文件生成在源文件同一目录下！',font="Helvetica 10 ")
    labelNotice.grid(row=4,column=0,columnspan=2)
    labelNotice = tk.Label(text = '        源文件加上后缀.enc为加密后的文件（二进制文件）',font="Helvetica 10 ")
    labelNotice.grid(row=5,column=0,columnspan=2,sticky='w')
    labelNotice = tk.Label(text = '        源文件加上后缀.enc.dec为解密后的文件',font="Helvetica 10 ")
    labelNotice.grid(row=6,column=0,columnspan=2,sticky='w')

    # 显示出来
    window.mainloop()