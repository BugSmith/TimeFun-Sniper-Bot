# TimeFun Sniper Bot

[![en](https://img.shields.io/badge/lang-English-blue.svg)](README.md) [![cn](https://img.shields.io/badge/����-����-red.svg)](README_CN.md)

����һ�����Twitter����time.fun��վ���Զ�����ʱ��ҵĻ����ˡ�

> **����״̬**: [�����] �Զ�����������ɲ�����ͨ����[�����] Twitter��ع�������ɡ�

## �����ص�

- ���@timedotfun Twitter�˺ŵ�ת��
- �Զ�ʶ���ƹ���û���
- �Զ���time.fun��Ϊ�ƹ��û�����ʱ���
- ���ӵ������е�Chrome�Ự�Ա���Cloudflare���
- ֧����������ȷ������

## [SAFE]��ȫ��ʾ

**��Ҫ**: �˻�������Ҫ��������Chrome�������TimeFun�˻�����ע�����°�ȫ�������

- ������ͨ��Զ�̵���ģʽ���ӵ�����Chrome�����������ܻ�ʹ�����������¶������Ӧ�ó���
- ����Chrome�û�����Ŀ¼����������Ϣ������cookies�ͱ��������
- `.env.utf8`�ļ�����������Ϣ
- ����������`.env.utf8`�ļ������Խ�ͼ��Chrome�û�����Ŀ¼
- ������ǰ�������룬ȷ�����������İ�ȫҪ��

## ��װ����

1. ��¡�˲ֿ�
2. ��װ����: `pip install -r requirements.txt`
3. ����`.env.utf8`�ļ������б�Ҫ�����ã��μ����ò��֣�

## ����˵��

������`.env.utf8`�ļ��������������ݣ�ע�⣺��Ҫ��ֵ�������ע�ͣ�����ܻᵼ�½������󣩣�

```
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

## ʹ�÷���

�����ṩ����������ģʽ��

### 1. ���ģʽ����Ҫ���ܣ�

ʹ��`timefun_buyer_en.py`�����Twitter���Զ�����

```bash
python timefun_buyer_en.py [ѡ��]
```

����ѡ�
- `--username` �� `-u`: ����Ҫ��ص�Twitter�û�����Ĭ�ϣ�timedotfun��
- `--interval` �� `-i`: ���ü�������룬Ĭ�ϣ�30��
- `--timezone` �� `-t`: ����ʱ��ƫ�ƣ�Ĭ�ϣ�8������ʱ�䣩
- `--max-tweets` �� `-m`: ����ÿ�μ��������������Ĭ�ϣ�5��
- `--skip-login-check`: ������¼���

### 2. ֱ�ӹ���ģʽ

ʹ��`timefun_buyer_en.py`ֱ�ӹ���ָ���û���ʱ��ң�

```bash
python timefun_buyer_en.py --buy �û��� [--skip-login-check]
```

### 3. ��֤ģʽ

��֤�û��Ƿ������time.fun��

```bash
python timefun_buyer_en.py --verify �û���
```

## �����ų�

### ��¼�������

����������޷���⵽���ѵ�¼����ʹ��ȷʵ�ѵ�¼������ʹ��`--skip-login-check`��־��

```bash
python timefun_buyer_en.py --skip-login-check
```

### ��ť�������

����������Ҳ�������ť��
1. �����ĿĿ¼�б���ĵ��Խ�ͼ��debug_screenshot_*.png��
2. �鿴����̨����еİ�ť�ı���Ϣ
3. ȷ������Chrome�Ự���ѵ�¼TimeFun

## �ļ�˵��

- `timefun_buyer_en.py` - �����򣬰�����غ͹�����
- `test_buy_en.py` - �����ܲ��Խű�
- `.env.utf8` - �������������ļ�

## ����״̬

��ǰ�汾: 1.0.0

### ����ɹ���
- [�����] �Զ�������
  - Chrome���ɺ�Զ�̵���
  - �Զ�����Chrome
  - �г�ҳ�浼��
  - ������������
  - ��ϸ������־�ͽ�ͼ
- [�����] Twitter��ع���
  - ʵʱ���@timedotfun�˺�
  - �Զ�ʶ���ƹ��û���

### �ƻ��еĹ���
- [�ƻ���] Web�����غͿ���
- [�ƻ���] ���˻�֧��

## ��Ҫ��ʾ

- ȷ������TimeFun�˻����㹻��USDC���
- ʹ���Զ����׹��ߴ��ڷ���
- ��ʼʱʹ��С�����Թ��ܣ�Ȼ��������
- �˻����˽�������Ŀ���ṩ
- �����߲����κβ�����ʧ���˻����⸺��

## ���֤

[MIT���֤](LICENSE) 