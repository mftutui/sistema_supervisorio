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
import java.util.logging.Level;
import java.util.logging.Logger;
import javax.swing.JOptionPane;

/**
 *
 * @author mftutui
 */
public class FilaDeMensagens {

    private static final String EXCHANGE_NAME = "logs";
    private static final String RETURN_NAME = "retorno";
    private static final String MEUIP = "192.168.0.8";
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
        factory.setUsername("the_user");
        factory.setPassword("the_pass");
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
                try {
                    fila.envia_confirmacao();
                } catch (TimeoutException ex) {
                    Logger.getLogger(FilaDeMensagens.class.getName()).log(Level.SEVERE, null, ex);
                }
            }

        };
        System.out.println("passou aqui");
        channel.basicConsume(queueName, true, consumer);
     

    }
    
    public void envia_confirmacao() throws IOException, TimeoutException{
           System.out.println("passou consume");
        ConnectionFactory factory_retorno = new ConnectionFactory();
        factory_retorno.setHost("localhost");
        Connection connection_retorno = factory_retorno.newConnection();
        Channel channel_retorno = connection_retorno.createChannel();

        channel_retorno.exchangeDeclare(RETURN_NAME, BuiltinExchangeType.FANOUT);

        String message = MEUIP;

        channel_retorno.basicPublish(RETURN_NAME, "", null, message.getBytes("UTF-8"));
        System.out.println(" [x] Sent '" + message + "'");
        channel_retorno.close();
        connection_retorno.close();

    }
    private void controle(String mensagem) {
        if (mensagem.matches("1")) {
            this.pausa();
        } else if (mensagem.matches("0")) {
            this.restart();
        } else if (mensagem.matches("10")) {
            this.fim();
        } else {
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
        while (!posicoes.isEmpty()) {
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
        //String pos8 = pos[8].substring(3, 7);
        //String pos9 = pos[9].substring(3, 7);

        posicoes.add(pos0);
        posicoes.add(pos1);
        posicoes.add(pos2);
        posicoes.add(pos3);
        posicoes.add(pos4);
        posicoes.add(pos5);
        posicoes.add(pos6);
        posicoes.add(pos7);
        //posicoes.add(pos8);
        //posicoes.add(pos9);

        //System.out.println(posicoes.get(0));
    }

    private void fim() {
        JOptionPane.showMessageDialog(this.pai, "Partida finalizada",
                "Opa!",
                JOptionPane.WARNING_MESSAGE);
        this.pai.travaBotoes();

    }

    public void enviaPosicoes() {
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
        if (this.status_modo == 1) {
            this.manual();
        } else {
            this.automatico();
        }
    }

    private void manual() {
        this.pai.modoManual();
        this.status_modo = 1;
    }

    private void automatico() {
        this.pai.modoAutomatico();
        this.status_modo = 0;
    }

};
