package flujoSimple;

import io.vertx.core.AbstractVerticle;
import io.vertx.core.Future;
import io.vertx.core.Handler;
import io.vertx.core.http.HttpServer;
import io.vertx.core.http.HttpServerRequest;

public class MyVerticle extends AbstractVerticle {
	private String x;
	private static HttpServer httpServer = null;
	public MyVerticle(String x) {
		this.x=x;
	}

	public MyVerticle() {
		// TODO Auto-generated constructor stub
	}

	@Override
    public void start(Future<Void> startFuture) {
		if(httpServer == null) {
	        httpServer = vertx.createHttpServer();
	        httpServer.requestHandler(new Handler<HttpServerRequest>() {
	            @Override
	            public void handle(HttpServerRequest request) {
	                System.out.println("incoming request!");
	            }
	        });
	        httpServer.listen(9999);
		}
		vertx.eventBus().consumer("anAddress", message -> {
            System.out.println("1 received message.body() = "
                + message.body());
        });

    }

    @Override
    public void stop(Future stopFuture) throws Exception {
        System.out.println("MyVerticle stopped!");
    }
}
