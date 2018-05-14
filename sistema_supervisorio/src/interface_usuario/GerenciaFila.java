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
public class GerenciaFila extends Thread{
    
   
   private static final String EXCHANGE_NAME = "logs";
   private JFPrincipal pai;
   public GerenciaFila(){
       
    }
    
    @Override
    public void run() {
        try {
            FilaDeMensagens fila = new FilaDeMensagens("guest","guest",pai);
            fila.starta(fila);
        }
             catch(Exception e){
                 System.out.println("erro fila");}
        
    }
    
     
}


