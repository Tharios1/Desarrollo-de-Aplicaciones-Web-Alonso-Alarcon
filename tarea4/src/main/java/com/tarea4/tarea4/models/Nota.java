package com.tarea4.tarea4.models;

import jakarta.persistence.*;


@Entity
@Table(name = "nota")
public class Nota {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;
    private Integer nota;

    @ManyToOne
    @JoinColumn(name = "aviso_id")
    private Aviso aviso;

    public Nota() {}
    public Nota(Aviso aviso, Integer nota) {
        this.aviso = aviso;
        this.nota = nota;
    }

    public Integer getNota() { return nota;}
    
}
