[�ļ��нṹ����]
1.arbiterĿ¼������д�Ĳ��Դ�������Ŀ¼,��������������Ҳ�ŵ��˴�
2.CoreServices\EventStructures\PlatformServices��"**API"����Ŀ¼��Thrift�ӿ��ļ����ɵ�Ŀ¼,�������
3.thriftĿ¼��python��Thrift������Ŀ¼,�������
4.configuration.cfg�������ļ�Ŀ¼�����Գ�������ʱ�Ĳ�����Ĭ�����ö��Ǵ��������ȡ��
  ����Ƚ���Ҫ�������ظĶ�
5.main.py�ǲ��Գ����������ģ�飬ͨ��ִ�������в��Գ���
6.python-unittest.log�ǲ��Գ���ִ�к����ɵ���־�ļ�


[�ó�������ʲô]
1.ͨ��Thrift�ӿ���Arbiter���һ����Ϊ"unittest-amtk"��host��10.101.0.181(��ͨ�������ļ���������)
  ��AMTK���͵��豸��������Ƿ���ȷ��ӵ����ݿ��DS
2.ͨ������beginStreamSession�鿴DS���ص�liveview��URL�Ƿ���ȷ
3.�����豸(Ĭ�Ͻ��豸��host��10.101.0.181��Ϊ10.101.0.182)���鿴���ݿ��и����Ƿ���ȷ��DS�Ƿ������ȷ��
  ���鿴���º��liveview
4.ɾ���豸�����鿴���ݿ��DS�Ƿ�ɾ����ȷ
--ע�⣺�����κ�һ��ִ��ʧ�ܣ�����Ϊ���Թ���ʧ��


[ִ�в���ǰ�ıر�����]
1.���Գ����CoreEngine��װ��ͬһ̨������(������ҪCoreEngine����������MySQL��Զ�̷���Ȩ��)
2.��������װ��Python����
3.��������װ��python MySQLdbģ��
--��鷽����
  ����python,���ն�����import MySQLdb
  ���������˵����װ�˸�ģ�飬�����˳�Python�նˣ�ִ��sudo apt-get install python-mysqldb
4.CoreEngine������ȷ��װ������Arbiter��MySQL��AMTK��DeviceServer��������


[������в��Գ���]
1.��python-unittestĿ¼������������������Ŀ¼��
2.ִ�� python main.py


[��β鿴���н��]
1.�鿴python-unittest.log,������ļ����������
 "Congratulations!!! Your testing is successful."�����ľ���,˵�����Գɹ������򣬲��Գ���ִ��ʧ��
2.�������ʧ�ܣ������������ļ��в���"ERROR"��"Exception"��Ϣ����λʧ��ԭ��




