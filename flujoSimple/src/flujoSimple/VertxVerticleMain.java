package flujoSimple;

import io.vertx.core.Vertx;

public class VertxVerticleMain {
	public static void main(String[] args) {
        Vertx vertx = Vertx.vertx();
        MyVerticle x = new MyVerticle();
        vertx.deployVerticle(x);
        System.out.println("xxx");

        vertx.deployVerticle(new MyVerticle("R1"));
        vertx.deployVerticle(new MyVerticle("R2"));

        try {
			Thread.sleep(3000);
		} catch (InterruptedException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
        vertx.deployVerticle(new EventBusSenderVerticle());
    }

}
