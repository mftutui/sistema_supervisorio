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
import java.util.ArrayList;
import java.util.concurrent.TimeoutException;
import javax.swing.JOptionPane;

/**
 *
 * @author mftutui
 */
public class FilaDeMensagens {

    private static final String EXCHANGE_NAME = "logs";
    
    private int status_modo;
    private String user;
    private ArrayList<String> posicoes;
    private String pass;
    private JFPrincipal pai;

    public FilaDeMensagens() {
    }

    ;
    public FilaDeMensagens(String user, String pass, JFPrincipal pai) {
        posicoes = new ArrayList<String>();
        this.user = user;
        this.pass = pass;
        this.pai = pai;
        try {
            this.starta(this);
        } catch (Exception e) {
        }

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
            FilaDeMensagens fila = f;

            @Override
            public void handleDelivery(String consumerTag, Envelope envelope,
                    AMQP.BasicProperties properties, byte[] body) throws IOException {
                message = new String(body, "UTF-8");
                System.out.println(" [x] Received '" + message + "'");
                fila.controle(message);

            }

        };

        channel.basicConsume(queueName, true, consumer);

    }
    
    private int inicio_de_partida=0;
    private int flag_pausa = 0;
    private void controle(String mensagem) {
      
         if (mensagem.matches("1") & flag_pausa==0) {
            this.pausa();
            flag_pausa = 1;
        } else if (mensagem.matches("0") & flag_pausa==1) {
            this.restart();
            flag_pausa=0;
        } 
        else if(mensagem.matches("0") & inicio_de_partida ==1){
                inicio_de_partida = 0;
               JOptionPane.showMessageDialog(this.pai, "Fim de partida",
                    "Opa!",
                    JOptionPane.WARNING_MESSAGE);
        this.pai.travaBotoes();
        } else {
            inicio_de_partida = 1;
            String bigmessage = mensagem;
            String[] separa = bigmessage.split("\"");
            String inicio = separa[3];
            String modo = separa[1];
            this.separaString(separa[4]);
            
            
            if (modo.matches("1") & inicio.matches("1")) {
                  JOptionPane.showMessageDialog(this.pai, "Partida iniciada - modo manual",
                    "Opa!",
                    JOptionPane.WARNING_MESSAGE);
                this.manual();
                this.enviaPosicoes();
                this.pai.iniciaTabela();
            }

            if (modo.matches("0") & inicio.matches("1")) {
                JOptionPane.showMessageDialog(this.pai, "Partida iniciada - automatico",
                    "Opa!",
                    JOptionPane.WARNING_MESSAGE);
                this.automatico();
                this.enviaPosicoes();
                this.pai.iniciaTabela();
                
            }

            
            
        }
    }

    private void separaString(String mensagem) {
        while(!posicoes.isEmpty()){
            posicoes.remove(0);
    }
        
        String[] pos = mensagem.split("]");

        String pos0 = pos[0].substring(4, 8);
        String pos1 = pos[1].substring(3, 7);
        String pos2 = pos[2].substring(3, 7);
        String pos3 = pos[3].substring(3, 7);
        String pos4 = pos[4].substring(3, 7);
        String pos5 = pos[5].substring(3, 7);
        String pos6 = pos[6].substring(3, 7);
        String pos7 = pos[7].substring(3, 7);
        String pos8 = pos[8].substring(3, 7);
        String pos9 = pos[9].substring(3, 7);

        posicoes.add(pos0);
        posicoes.add(pos1);
        posicoes.add(pos2);
        posicoes.add(pos3);
        posicoes.add(pos4);
        posicoes.add(pos5);
        posicoes.add(pos6);
        posicoes.add(pos7);
        posicoes.add(pos8);
        posicoes.add(pos9);
        
        //System.out.println(posicoes.get(0));
    }
  
    
    public void enviaPosicoes(){
        this.pai.recebePosicoes(posicoes);
    }
    private void pausa() {
         JOptionPane.showMessageDialog(this.pai, "Partida parada",
                    "Opa!",
                    JOptionPane.WARNING_MESSAGE);
        this.pai.travaBotoes();
    }

    private void restart() {
          JOptionPane.showMessageDialog(this.pai, "Partida voltou",
                    "Opa!",
                    JOptionPane.WARNING_MESSAGE);
        this.pai.liberaBotoes();
        if (this.status_modo == 2) {
            this.manual();
        } else if(this.status_modo == 1) {
            this.automatico();
        }
        else {
            this.pai.travaBotoes();
        }
    }

    private void manual() {
        this.pai.modoManual();
        this.status_modo = 2;
    }

    private void automatico() {
        this.pai.modoAutomatico();
        this.status_modo = 1;
    }

};
