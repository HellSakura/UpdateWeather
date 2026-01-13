import base64
import os
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives import serialization

def generate_eddsa_keypair():
    """
    生成适用于和风天气 JWT 认证的 Ed25519 密钥对。
    和风天气控制台需要：
    1. 公钥 (Public Key): 用于上传到和风控制台。
    2. 私钥 (Private Key): 用于程序生成 JWT（PKCS#8 PEM 格式）。
    """
    print("正在生成 Ed25519 密钥对...")

    # 1. 生成 Ed25519 私钥对象
    private_key = ed25519.Ed25519PrivateKey.generate()
    
    # 2. 导出私钥为 PEM 格式 (PKCS#8)，这是 PyJWT 库推荐的格式
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    ).decode('utf-8')

    # 3. 导出公钥的原始字节并进行 Base64 编码 (这是上传到和风天气控制台的内容)
    public_key = private_key.public_key()
    public_bytes = public_key.public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw
    )
    # 和风控制台通常需要 Base64 后的公钥
    public_base64 = base64.b64encode(public_bytes).decode('utf-8')

    # 保存到文件
    with open("private_key.pem", "w") as f:
        f.write(private_pem)
    
    with open("public_key.txt", "w") as f:
        f.write(public_base64)

    print("\n" + "="*60)
    print("密钥对生成成功！")
    print("="*60)
    print(f"1. 公钥 (Base64格式): {os.path.abspath('public_key.txt')}")
    print("请打开此文件，将内容复制并粘贴到和风天气控制台。")
    print("-" * 60)
    print(f"2. 私钥 (PEM格式): {os.path.abspath('private_key.pem')}")
    print("使用 PyJWT 时，请直接读取此文件的内容作为 private_key。")
    print("对于本程序的 config.ini，请将 PEM 内部的 Base64 核心内容填入即可。")
    print("="*60)
    print("⚠️ 请妥善保管您的私钥 (private_key.pem)，切勿泄露！")

if __name__ == "__main__":
    try:
        generate_eddsa_keypair()
    except Exception as e:
        print(f"发生错误: {e}")
