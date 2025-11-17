package com.tarea4.tarea4.models;
import jakarta.persistence.*;
import java.time.LocalDate;

@Entity
@Table(name = "aviso_adopcion")
public class Aviso {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;

    @Column(name = "fecha_ingreso")
    private LocalDate fechaPublicacion;

    @ManyToOne
    @JoinColumn(name = "comuna_id")
    private Comuna comuna;

    private String sector;
    private Integer cantidad;
    private String tipo;
    private Integer edad;

    @Transient
    private Double promedio;

    public Integer getId(){ return id; }
    public void setId(Integer id){ this.id = id; }

    public LocalDate getFechaPublicacion(){ return fechaPublicacion; }
    public void setFechaPublicacion(LocalDate fechaPublicacion){ this.fechaPublicacion = fechaPublicacion; }

    public Comuna getComuna(){ return comuna; }
    public void setComuna(Comuna comuna){ this.comuna = comuna; }

    public String getSector(){ return sector; }
    public void setSector(String sector){ this.sector = sector; }

    public Integer getCantidad(){ return cantidad; }
    public void setCantidad(Integer cantidad){ this.cantidad = cantidad; }

    public String getTipo(){ return tipo; }
    public void setTipo(String tipo){ this.tipo = tipo; }

    public Integer getEdad(){ return edad; }
    public void setEdad(Integer edad){ this.edad = edad; }

    public Double getPromedio(){ return promedio; }
    public void setPromedio(Double promedio){ this.promedio = promedio; }
}
