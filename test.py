from urllib.parse import quote, unquote

# 编码
url = "http://example-node-2/authors/5f57808f-0bc9-4b3d-bdd1-bb07c976d12d"
encoded_url = quote(url)
print(encoded_url)  # 输出: http%3A%2F%2Fexample-node-2%2Fauthors%2F5f57808f-0bc9-4b3d-bdd1-bb07c976d12d

# 解码
decoded_url = unquote(encoded_url)
print(decoded_url)  # 输出: http://example-node-2/authors/5f57808f-0bc9-4b3d-bdd1-bb07c976d12d