package server;

/**
 * Created by Timothy on 8/15/16.
 */
import dbmanager.DatabaseConfig;
import dbmanager.DatabaseService;
import io.netty.buffer.ByteBuf;
import io.netty.channel.ChannelHandlerContext;
import io.netty.channel.ChannelInboundHandlerAdapter;
import io.netty.handler.codec.http.HttpObject;

import java.io.IOException;

/**
 * Handles a server-side channel.
 */
public class DiscardServerHandler extends ChannelInboundHandlerAdapter { // (1)

    @Override
    public void channelRead(ChannelHandlerContext ctx, Object msg) { // (2)
        if (msg instanceof HttpObject) {
            System.out.println("It's an http object");
//            ((ByteBuf) msg).release();
        } else {
            System.out.println("It's NOT an http object");
            ((ByteBuf) msg).release();
        }
        DatabaseConfig config = null;
        try {
            config = new DatabaseConfig("./db/config/items_config");
        } catch (IOException e) {
            e.printStackTrace();
            System.out.println("Could not load config.");
        }
        DatabaseService service = new DatabaseService(config);
        ctx.writeAndFlush("Test stf");
        ctx.writeAndFlush(msg);
        ctx.close();
    }

    @Override
    public void exceptionCaught(ChannelHandlerContext ctx, Throwable cause) { // (4)
        // Close the connection when an exception is raised.
        cause.printStackTrace();
        ctx.close();
    }
}
