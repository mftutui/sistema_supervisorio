/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package interface_usuario;

import java.awt.Container;
import javax.ws.rs.ClientErrorException;
import javax.ws.rs.client.Client;
import javax.ws.rs.client.WebTarget;
import java.lang.Exception;
import com.rabbitmq.client.*;
import java.lang.Exception;
import com.rabbitmq.client.*;

import java.io.IOException;
import java.util.concurrent.TimeoutException;

import java.io.IOException;
import java.util.concurrent.TimeoutException;

/**
 *
 * @author mftutui
 */
public class FilaDeMensagens {

    private static final String EXCHANGE_NAME = "logs";

    private String user;

    private String pass;
    private JFPrincipal pai;

    
    public FilaDeMensagens(){};
    public FilaDeMensagens(String user, String pass, JFPrincipal pai) {
        this.user = user;
        this.pass = pass;
        this.pai =  pai;
        try{
        this.starta(this);
    } catch (Exception e){}
        
    }
    
    
    public void starta(final FilaDeMensagens f) throws Exception {
        ConnectionFactory factory = new ConnectionFactory();
        factory.setUsername("guest");
        factory.setPassword("guest");
        factory.setVirtualHost("/");
        factory.setHost("localhost");
        factory.setPort(5672);
        Connection connection = factory.newConnection();
        Channel channel = connection.createChannel();
        
        channel.exchangeDeclare(EXCHANGE_NAME, "fanout");
        String queueName = channel.queueDeclare().getQueue();
        channel.queueBind(queueName, EXCHANGE_NAME, "");

        System.out.println(" [*] Waiting for messages. To exit press CTRL+C");

        Consumer consumer;
        consumer = new DefaultConsumer(channel) {
            public String message;
            
            
            @Override
            public void handleDelivery(String consumerTag, Envelope envelope,
                AMQP.BasicProperties properties, byte[] body) throws IOException {
                message = new String(body, "UTF-8");
                System.out.println(" [x] Received '" + message + "'");
                f.controle(message);
                
            }
         
        };
        
        channel.basicConsume(queueName, true, consumer);
        
    }
   
   
    
    private void controle(String mensagem){
        if(mensagem.matches("pausa=1")){
            this.pai.travaBotoes();
        }
        
        if(mensagem.matches("pausa=0")){
            this.pai.liberaBotoes();
        }
        
    }
    
    private void pausa(){
        this.pai.travaBotoes();
    }
    
    private void restart(){
       this.pai.liberaBotoes();
    }
};


