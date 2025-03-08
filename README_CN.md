# TimeFun Sniper Bot

����һ�����Twitter����time.fun��վ���Զ�����ʱ��ҵĻ����ˡ�

> **��������**: ? �Զ����빦������ɲ�����ͨ�������Գɹ�ʶ��͵������ť��? ���ؼ�ع������ڿ����С�

## �����ص�

- ���@timedotfun Twitter�˺ŵ�ת��
- �Զ�ʶ���ƹ���û���
- �Զ���time.fun��Ϊ�ƹ��û�����ʱ���
- ���ӵ������е�Chrome�Ự�Ա���Cloudflare���
- ֧����������ȷ������

## ?? ��ȫ��ʾ

**��Ҫ**: �˻�������Ҫ��������Chrome�������TimeFun�˻�����ע�����°�ȫ�������

- ������ͨ��Զ�̵���ģʽ���ӵ�����Chrome�����������ܻ�ʹ�����������¶������Ӧ�ó���
- ����Chrome�û�����Ŀ¼����������Ϣ������cookies�ͱ��������
- `.env.utf8`�ļ��������е�API��Կ��ƾ��
- ����������`.env.utf8`�ļ������Խ�ͼ��Chrome�û�����Ŀ¼
- ������ǰ�������룬ȷ�����������İ�ȫҪ��

## ��װ����

1. ��¡�˲ֿ�
2. ��װ����: `pip install -r requirements.txt`
3. ����`.env.utf8`�ļ������б�Ҫ�����ã��μ����ò��֣�

## ����˵��

������`.env.utf8`�ļ��������������ݣ�ע�⣺��Ҫ��ֵ�������ע�ͣ�����ܻᵼ�½������󣩣�

```
# Twitter APIƾ��
TWITTER_API_KEY=your_api_key
TWITTER_API_SECRET=your_api_secret
TWITTER_ACCESS_TOKEN=your_access_token
TWITTER_ACCESS_TOKEN_SECRET=your_access_token_secret

# TimeFun�˻���Ϣ
TIMEFUN_EMAIL=your_email
TIMEFUN_PASSWORD=your_password

# ��������
BUY_AMOUNT=2
MAX_BUY_ATTEMPTS=3
BUY_DELAY=2

# �������
CHECK_INTERVAL=60
HEADLESS=False

# Chrome����
# ��Ҫ������������Ϊ����Chrome�û�����Ŀ¼
CHROME_USER_DATA_DIR=C:\\Users\\YourUsername\\AppData\\Local\\Google\\Chrome\\User Data
```

### Chrome�û�����Ŀ¼

`CHROME_USER_DATA_DIR`������**�����**������ָ������Chrome�û�����Ŀ¼��

- **Windows:** ͨ��Ϊ `C:\Users\�����û���\AppData\Local\Google\Chrome\User Data`
- **Mac:** ͨ��Ϊ `~/Library/Application Support/Google/Chrome`
- **Linux:** ͨ��Ϊ `~/.config/google-chrome`

ȷ����Windows·����ʹ��˫��б��(`\\`)��

### ��������

- `TIMEFUN_EMAIL`: ����TimeFun�˻����䣨�����ο���
- `TIMEFUN_PASSWORD`: ����ʹ�õ�Ϊ�˼����Զ�����
- `BUY_AMOUNT`: ÿ�ι����USDC���
- `MAX_BUY_ATTEMPTS`: ������Դ���
- `BUY_DELAY`: �������֮����ӳ٣��룩
- `CHECK_INTERVAL`: ���Twitter�ļ�����룩
- `HEADLESS`: ʹ������Chrome�ỰʱӦ����ΪFalse

## Chrome����

�����˿������ӵ������е�Chromeʵ�����Զ�����Chrome��

### ѡ��1���ֶ�����Chrome���Ƽ���

1. �ر�����Chrome����
2. ʹ������������������Զ�̵��Թ��ܵ�Chrome��

   **Windows:**
   ```
   "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="C:\Users\�����û���\AppData\Local\Google\Chrome\User Data"
   ```

   **Mac:**
   ```
   /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222 --user-data-dir="~/Library/Application Support/Google/Chrome"
   ```

   **Linux:**
   ```
   google-chrome --remote-debugging-port=9222 --user-data-dir="~/.config/google-chrome"
   ```

3. �ڴ򿪵�Chrome�����У�������https://time.fun����¼
4. ����Chrome�򿪲�����
5. Ȼ�����л�����

### ѡ��2���Զ�����Chrome

��������������������������ڿ����Զ�ʹ����ȷ�Ĳ�������Chrome��
- Chrome��δ��Զ�̵���ģʽ����
- ������`.env.utf8`�ļ�����ȷ������`CHROME_USER_DATA_DIR`

## ��������˵��

�����˻�ֱ�ӵ������û����г���ǩҳ�����磬https://time.fun/username?tab=market��������������ҵ�����ť��������

1. ����ʹ�ø���ѡ�����ҵ�����ť
2. �ҵ���������ť
3. �������õ�USDC���
4. ������յ�"ȷ�ϲ�����"��ť��ɹ���

����������֧�������������̣�
- ���ȵ��"����X���ӣ��۸�$Y"��ť
- Ȼ����"ȷ�ϲ�����X���ӣ��۸�$Y"��ť

## �����ų�

### ��¼�������

����������޷���⵽���ѵ�¼����ʹ��ȷʵ�ѵ�¼������ʹ��`--skip-login-check`��־��

```
python main.py --skip-login-check
```

�������ڲ��ԣ�

```
python test_buy_en.py <�û���> --skip-login-check
```

### ��ť�������

����������Ҳ�������ť��
1. �����ĿĿ¼�б���ĵ��Խ�ͼ
2. �鿴����̨����еİ�ť�ı���Ϣ
3. ȷ������Chrome�Ự���ѵ�¼TimeFun

## ����

������������֮ǰ�����������в��ԣ�

1. ������������: `python test_connection.py`
2. ���Թ�����: `python test_buy_en.py <�û���>`
3. ����Twitter���: `python test_monitor.py`

## ʹ�÷���

����������

```
python main.py
```

���򽫼��@timedotfun��Twitter�˺ţ����Զ�Ϊ�ƹ��û�����ʱ��ҡ�

## �ļ�˵��

- `main.py` - ����Twitter��غ�TimeFun�����������
- `twitter_monitor.py` - Twitter���ģ��
- `timefun_buyer_en.py` - TimeFun����ģ��
- `test_*.py` - ���ֲ��Խű�
- `.env.utf8` - ������������

## ����״̬

��ǰ�汾: 1.0.0

- ? �Զ����빦�������
  - ? Chrome������Զ�̵���
  - ? �Զ�����Chrome
  - ? �г���ǩҳ����
  - ? ������������
  - ? ��ϸ������־�ͽ�ͼ
- ? ���ؼ�ع��ܿ�����
  - ? ʵʱ���@timedotfun�˺�
  - ? �Զ�ʶ���ƹ��û���
- ? �ƻ�����
  - ? �Ľ�������ͻָ�����
  - ? Web�����غͿ���
  - ? ���˻�֧��

## ��Ҫ��ʾ

- ȷ������TimeFun�˻����㹻��USDC���
- ʹ���Զ����׹��ߴ��ڷ���
- ��ʼʱʹ��С�����Թ��ܣ�Ȼ��������
- �˻����˽�������Ŀ���ṩ
- �����߲����κβ�����ʧ���˻����⸺��

## ���֤

[MIT���֤](LICENSE) 