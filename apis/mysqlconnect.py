dbconfig = {
	"host":"localhost",
	"user":"",
	"password":"",
	"database":"week"
}
mydbpool = pooling.MySQLConnectionPool(
	pool_name = "mypool",
	pool_size = 5,
    pool_reset_session = True,
    **dbconfig
) 