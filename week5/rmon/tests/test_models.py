# coding=utf-8

from rmon.models import Server
from rmon.common.rest import RestException


class TestServer:
    """ 测试 Server 相关功能
    """

    def test_save(self, db):
        """ save method
        """
        assert Server.query.count() == 0
        server = Server(name='test', host='127.0.0.1')
        server.save()
        assert Server.query.count() == 1
        assert Server.query.first() == server

    def test_delete(self, db, server):
        """delete method
        """
        assert Server.query.count() == 1
        server.delete()
        assert Server.query.count() == 0

    def test_ping_sucess(self, db, server):
        """
        测试 Server.ping 方法执行成功
            需要保证 Redis 服务器监听在 127.0.0.1:6379 地址
        :param db:
        :param server:
        :return:
        """
        assert server.ping() is True

    def test_ping_faild(self, db):
        """
        测试 Server.ping 方法执行失败
            Server.ping 方法执行失败时, 会抛出 RestException 异常
        :param db:
        :return:
        """
        server = Server(name='test', host='127.0.0.1', port=6399)
        try:
            server.ping()
        except RestException as e:
            assert e.code == 400
            assert e.message == 'redis server %s can not connected' % server.host
