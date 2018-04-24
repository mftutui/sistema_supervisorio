/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package interface_usuario;

import java.lang.Exception;

        
/**
 *
 * @author aluno
 */
public class GerenciaThread extends Thread{
    
   private String direcao;
   
    ClienteRobot c = new ClienteRobot();
    public GerenciaThread(String direcao){
    this.direcao = direcao;
    
    }
    
    @Override
    public void run() {
        try {
            c.movimenta(this.direcao);
        }
             catch(Exception e){
                 System.out.println("erro");}
        
    }
}



