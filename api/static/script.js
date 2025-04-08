let canvas = document.getElementById("drawingCanvas");
let context = canvas.getContext("2d");
let drawing = false;

// Configura el grosor de la línea
context.lineWidth = 10;

// Ajusta la posición del puntero para dibujar correctamente
function getMousePos(canvas, event) {
    const rect = canvas.getBoundingClientRect();
    return {
        x: event.clientX - rect.left,
        y: event.clientY - rect.top
    };
}

// Comienza a dibujar
canvas.addEventListener("mousedown", (event) => {
    drawing = true;
    const pos = getMousePos(canvas, event);
    context.moveTo(pos.x, pos.y);
});

// Dibuja mientras se mueve el mouse
canvas.addEventListener("mousemove", (event) => {
    if (drawing) {
        const pos = getMousePos(canvas, event);
        context.lineTo(pos.x, pos.y);
        context.stroke();
    }
});

// Detén el dibujo
canvas.addEventListener("mouseup", () => {
    drawing = false;
});

// Limpia el canvas, el resultado de predicción y elimina las imágenes generadas
function clearCanvas() {
    context.clearRect(0, 0, canvas.width, canvas.height);
    context.beginPath();
    context.fillStyle = "white";
    context.fillRect(0, 0, canvas.width, canvas.height);
    document.getElementById("predictionResult").innerText = "";

    // Solicitud para eliminar las imágenes generadas
    fetch('/clear-images', {
        method: 'POST'
    }).then(response => {
        if (response.ok) {
            console.log("Imágenes eliminadas correctamente.");
        } else {
            console.error("Error al eliminar las imágenes.");
        }
    });
}

// Mostrar los resultados de predicción con porcentajes, números y la imagen original
function displayPredictionResults(results, originalImage) {
    const resultContainer = document.getElementById("predictionResult");
    resultContainer.innerHTML = `
    <div class="card h-100">
        <div class="card-header">
            <h2>Resultados de Predicción</h2>
        </div>
        <div class="card-body">
            <div class="row">
                <div class="col-md-6">
                    <h3>Original</h3>
                    <img src="${originalImage}" alt="Original Image" class="img-fluid" style="width: 200px;">
                </div>
                <div class="col-md-6">
                    <h3>Procesada</h3>
                    ${results.map(result => `<img src="${result.processed_image}" alt="Processed Image" class="img-fluid" style="width: 200px;">`).join("")}
                </div>
            </div>
            <div class="table-responsive">
                <table class="table table-bordered table-responsive-sm">
                    <thead class="thead-dark">
                        <tr>
                            <th scope="col">Porcentajes</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${results.map(result => `
                            <tr>
                                <td>
                                    ${result.percentages.map((p, i) => `
                                        <div class="mb-2">
                                            <strong>Número ${i}: ${parseInt(p)}%</strong>
                                            <div class="progress">
                                                <div class="progress-bar" role="progressbar" style="width: ${parseInt(p)}%" aria-valuenow="${parseFloat(p) * 100}" aria-valuemin="0" aria-valuemax="100">
                                                    ${p}
                                                </div>
                                            </div>
                                        </div>
                                    `).join("")}
                                </td>
                            </tr>
                        `).join("")}
                    </tbody>
                </table>
            </div>
        </div>
        <div class="card-footer">
            <button class="btn btn-block btn-secondary" onclick="clearCanvas()">Borrar</button>
        </div>
    </div>
    `;
}

// Convierte el canvas en una imagen y la envía a la API para predecir
function predictDigit() {
    let image = canvas.toDataURL("image/png");

    // Convierte la imagen a Blob
    fetch(image)
        .then(res => res.blob())
        .then(blob => {
            let formData = new FormData();
            formData.append('image', blob, 'image.png');

            fetch('/predict', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                displayPredictionResults(data.results, data.original_image);
            });
        });
}