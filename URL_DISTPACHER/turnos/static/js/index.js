let medicos = [];

const listarMedicos = async (idEspecialidad) => {
    try {
        const response = await fetch(`./medicos/${idEspecialidad}`);
        const data = await response.json();

        if (data.message === "Success") {
            medicos = data.medicos;
            let opciones = ``;
            medicos.forEach((medico) => {
                opciones += `<option value='${medico.id}'>${medico.nombre+' '+medico.apellido }</option>`;
            });
            cboMedico.innerHTML = opciones;
         } else {
            let opciones = ``;
            alert("Especialidades no encontrados...");
            cboMedico.innerHTML = opciones;
        }
    } catch (error) {
        console.log(error);
    }
};

const listarEspecialidades = async () => {
    try {
        const response = await fetch("./especialidades");
        const data = await response.json();

        if (data.message === "Success") {
            let opciones = ``;
            data.especialidades.forEach((especialidad) => {
                opciones += `<option value='${especialidad.id}'>${especialidad.nombre}</option>`;
            });
            cboEspecialidad.innerHTML = opciones;
            listarCiudades(data.especialidades[0].id);
        } else {
            alert("Especiadlidades no encontrados...");
        }
    } catch (error) {
        console.log(error);
    }
};


const cargaInicial = async () => {
    await listarEspecialidades();

    cboEspecialidad.addEventListener("change", (event) => {
        listarMedicos(event.target.value);
    });


};

window.addEventListener("load", async () => {
    await cargaInicial();
});