$(document).ready(function () {
    // Initialize DataTables
    var packagesTable = $('#management_table').DataTable({
        language: {
            url: 'https://cdn.datatables.net/plug-ins/2.1.8/i18n/es-MX.json',
        }
    });

    var packageTable = $('#select_package_table').DataTable({
        language: {
            url: 'https://cdn.datatables.net/plug-ins/2.1.8/i18n/es-MX.json',
        },
        select: {
            style: 'multi', // Permite selección múltiple
        },
    });

    // Almacena los datos seleccionados
    var selectedPackages = [];

    // Maneja el evento de selección
    packageTable.on('select', function (e, dt, type, indexes) {
        if (type === 'row') {
            var data = packageTable
                .rows(indexes)
                .data()
                .pluck(0)[0];

            selectedPackages.push(data);
            $('input[name="PCK_packagesId"]').val(selectedPackages);
            console.log($('input[name="PCK_packagesId"]').val());

        }
    });

    // Maneja el evento de deselección
    packageTable.on('deselect', function (e, dt, type, indexes) {
        if (type === 'row') {
            var data = packageTable
                .rows(indexes)
                .data()
                .pluck(0)[0];

            selectedPackages = selectedPackages.filter(function (item) {
                return item !== data;
            });
            $('input[name="PCK_packagesId"]').val(selectedPackages);
            console.log($('input[name="PCK_packagesId"]').val());
        }
    });

    var selectPackageModal = new bootstrap.Modal(document.getElementById('selectPackageModal'));

    $('body').on('click', '#add-record-btn', function () {
        selectPackageModal.show();
    });

    $('#closeSelectPackageModalFooter').on('click', function () {
        selectPackageModal.hide();
    });
});
