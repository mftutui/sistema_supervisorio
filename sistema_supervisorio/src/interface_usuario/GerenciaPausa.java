/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package interface_usuario;

import java.lang.Exception;
import com.rabbitmq.client.*;

import java.io.IOException;
import java.util.concurrent.TimeoutException;
        
/**
 *
 * @author aluno
 */
public class GerenciaPausa extends Thread{
    
   
   private static final String EXCHANGE_NAME = "logs";
   private JFPrincipal pai;
   public GerenciaPausa(){
       
    }
    
    @Override
    public void run() {
        try {
            
        this.starta();
        }
             catch(Exception e){
                 System.out.println("erro fila");}
        
    }
    
     public void starta() throws Exception {
        ConnectionFactory factory = new ConnectionFactory();
        factory.setHost("localhost");
        Connection connection = factory.newConnection();
        Channel channel = connection.createChannel();

        channel.exchangeDeclare(EXCHANGE_NAME, "fanout");
        String queueName = channel.queueDeclare().getQueue();
        channel.queueBind(queueName, EXCHANGE_NAME, "");

        System.out.println(" [*] Waiting for messages. To exit press CTRL+C");

        Consumer consumer;
       consumer = new DefaultConsumer(channel) {
           @Override
           public void handleDelivery(String consumerTag, Envelope envelope,
                   AMQP.BasicProperties properties, byte[] body) throws IOException {
               String message = new String(body, "UTF-8");
               System.out.println(" [x] Received '" + message + "'");
               if(message.matches("1")){
                   pai.trava(1);
               } else {
                   pai.trava(0);
               }
           }
       };
        channel.basicConsume(queueName, true, consumer);
    }
}


