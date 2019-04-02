import re
from bs4 import BeautifulSoup
text = "<script language='javascript'>alert('Username Code Wrong!');history.go(-1);</script>"
# text = "Username"
pattern = re.compile(r"alert\(\'Usernam")
if re.search(pattern, text):
    print("True")
else:
    print("False")

data = """
<script language='javascript'>
alert('UserName or Password Wrong!');
history.go(-1);
</script>
"""
if re.search(r"(?<=U).*?(?=e)", data):
    print("True")
else:
    print("False")
